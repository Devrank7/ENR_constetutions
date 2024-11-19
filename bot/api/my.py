from abc import ABC, abstractmethod

from aiogram.enums import ChatMemberStatus
from aiogram.types import Message

from bot.api.permision import my_permission_has
from db.mongo.bot_settings import ChangesUsers, update_bot_settings


class MyChange(ABC):

    def __init__(self, message: Message):
        self.message = message

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
    async def _delete_message(self):
        bot = self.message.bot
        await bot.delete_message(self.message.chat.id, self.message.message_id)
        return True

    async def _change(self) -> bool:
        has = await my_permission_has(self.message,
                                      [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR])
        if has and self.message.text:
            text = self.message.text
            reply = self.message.reply_to_message
            await self._delete_message()
            if reply:
                await self.message.bot.send_message(self.message.chat.id, text, reply_to_message_id=reply.message_id)
            else:
                await self.message.bot.send_message(self.message.chat.id, text)
            return True
        return False
