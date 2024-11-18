import datetime
from abc import ABC, abstractmethod

from aiogram.enums import ChatMemberStatus
from aiogram.types import Message, ChatPermissions


async def my_permission_has(message: Message, permissions: list[ChatMemberStatus]):
    chat_id = message.chat.id
    bot_id = (await message.bot.get_me()).id
    bot_member = await message.bot.get_chat_member(chat_id, bot_id)
    return bot_member.status in permissions


class Restrict(ABC):

    def __init__(self, message: Message):
        self.message = message

    async def restrict(self):
        try:
            await self._relative_restrict()
        except Exception as e:
            await self.message.answer(str(e))

    @abstractmethod
    async def _relative_restrict(self):
        raise NotImplementedError


class AnswerBan(Restrict):

    def __init__(self, message: Message, minutes: int = 1, forever: bool = False):
        super().__init__(message)
        if minutes <= 0 or minutes > 3600:
            raise ValueError("Укажите дапозон от 1 до 3600")
        self.minutes = minutes
        self.forever = forever

    async def _relative_restrict(self):
        if self.forever:
            await self.message.bot.restrict_chat_member(
                chat_id=self.message.chat.id,
                user_id=self._get_user_id(),
                permissions=ChatPermissions(can_send_messages=False),
            )
            await self.message.answer(f"Ползователь {self._get_first_name()} был за баннен на всегда.")
            return
        await self.message.bot.restrict_chat_member(
            chat_id=self.message.chat.id,
            user_id=self._get_user_id(),
            permissions=ChatPermissions(can_send_messages=False),
            until_date=datetime.datetime.now() + datetime.timedelta(minutes=self.minutes)
        )
        await self.message.answer(
            f"Пользователь {self._get_first_name()} был за баннен на {self.minutes} минут.")

    def _get_user_id(self):
        return self.message.from_user.id

    def _get_first_name(self):
        return self.message.from_user.first_name


class ReplyBan(AnswerBan):

    async def _relative_restrict(self):
        if self.message.reply_to_message is None:
            await self.message.answer("Закрепите сообщение пользователя которого вы хочете за баннить.👆")
            return
        return await super()._relative_restrict()

    def _get_user_id(self):
        return self.message.reply_to_message.from_user.id

    def _get_first_name(self):
        return self.message.reply_to_message.from_user.first_name


class AnswerUnban(Restrict):
    async def _relative_restrict(self):
        await self.message.bot.restrict_chat_member(
            chat_id=self.message.chat.id,
            user_id=self._get_user_id(),
            permissions=ChatPermissions(
                can_send_messages=True,
                can_send_photos=True,
                can_send_voice=True,
                can_send_polls=True,
                can_send_documents=True,
                can_send_audios=True,
                can_send_videos=True,
                can_invite_users=True,
                can_pin_messages=True,
                can_send_other_messages=True,
                can_send_video_notes=True,
                can_send_voice_notes=True
            ),
        )
        await self.message.answer(f"Разбаннен {self._get_first_name()}")

    def _get_user_id(self):
        return self.message.from_user.id

    def _get_first_name(self):
        return self.message.from_user.first_name


class ReplyUnban(AnswerUnban):
    async def _relative_restrict(self):
        if self.message.reply_to_message is None:
            await self.message.answer("Закрепите сообщение пользователя которого вы хочете раз баннить.👆")
            return
        await super()._relative_restrict()

    def _get_user_id(self):
        return self.message.reply_to_message.from_user.id

    def _get_first_name(self):
        return self.message.reply_to_message.from_user.first_name
