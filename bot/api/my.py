from abc import ABC, abstractmethod

from aiogram.enums import ChatMemberStatus, ReactionTypeType
from aiogram.types import Message, ReactionTypeEmoji

from bot.api.permision import my_permission_has
from bot.api.react import React
from db.mongo.bot_settings import ChangesUsers, update_bot_settings


class MyChange(ABC):

    def __init__(self, message: Message):
        self.message = message

    async def _delete_message(self):
        bot = self.message.bot
        await bot.delete_message(self.message.chat.id, self.message.message_id)
        return True

    def __need_to_change(self, user_id: int) -> bool:
        users_ids = update_bot_settings(ChangesUsers())
        return user_id in users_ids

    async def update(self) -> bool:
        if not self.__need_to_change(self.message.from_user.id):
            return False
        return await self._change()

    @abstractmethod
    async def _change(self) -> bool:
        raise NotImplementedError


class UpdateMessage(MyChange):

    async def _change(self) -> bool:
        has = await my_permission_has(self.message,
                                      [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR])
        if has and self.message.text:
            bot = self.message.bot
            text = self.message.text
            reply = self.message.reply_to_message
            await self._delete_message()
            if reply:
                await bot.send_message(self.message.chat.id, text, reply_to_message_id=reply.message_id)
            else:
                await bot.send_message(self.message.chat.id, text)
            return True
        return False


class ReactionMessage(MyChange):
    async def react(self):
        if not self.message.text.startswith("react_"):
            return False
        if not self.message.reply_to_message:
            return False
        bot = self.message.bot
        emo = self.message.text.split("_")[1].upper()
        try:
            emo = React[emo]
        except KeyError:
            return False
        await self._delete_message()
        emoji = ReactionTypeEmoji(emoji=emo.value)
        await bot.set_message_reaction(self.message.chat.id, self.message.reply_to_message.message_id,
                                       [emoji])
        return True

    async def _change(self) -> bool:
        has = await my_permission_has(self.message,
                                      [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR])
        if has and self.message.text:
            return await self.react()
