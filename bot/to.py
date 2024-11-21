from abc import ABC, abstractmethod

from aiogram import Bot
from aiogram.exceptions import TelegramAPIError
from aiogram.types import Message, ChatPermissions

from bot.exception.exc import ArgsException, NoChatException
from bot.util.util import to_json
from telethon.tl.types import Message as TelethonMessage


class MessageInfo:
    def __init__(self, date, message_id, text):
        self.date = date
        self.message_id = message_id
        self.text = text


async def get_history(bot: Bot, chat_id: int, limit: int = 100) -> list[MessageInfo]:
    return []


class To(ABC):
    def __init__(self, message: Message):
        self.message = message

    @abstractmethod
    async def send(self):
        raise NotImplementedError


class ToChat(To):
    async def check_chat(self, chat_id):
        try:
            chat = await self.message.bot.get_chat(chat_id)
            print("chat title:", chat.title)
        except Exception as e:
            raise NoChatException(e)

    def __init__(self, message: Message, json_loader: str, bot: Bot):
        super().__init__(message)
        self.json_dict = to_json(json_loader)
        chat_id = self.json_dict.get("chat_id")
        if not chat_id:
            raise ArgsException("No chat_id in json_loader")
        self.chat_id = int(chat_id)
        text = self.json_dict.get("text")
        if not text:
            raise ArgsException("No text in json_loader")
        self.text = text
        self.bot = bot

    async def send(self):
        await self.check_chat(self.chat_id)
        reply_id = self.json_dict.get("reply_id")
        if reply_id:
            await self.message.bot.send_message(self.chat_id, self.text, reply_to_message_id=reply_id)
        else:
            await self.message.bot.send_message(chat_id=self.chat_id, text=self.text)


class ToChatUnban(ToChat):

    def __init__(self, message: Message, json_loader: str, bot: Bot):
        super().__init__(message, json_loader, bot)

    async def send(self):
        await self.check_chat(self.chat_id)
        user_id = self.json_dict.get("user_id")
        await self.bot.restrict_chat_member(
            chat_id=self.chat_id,
            user_id=int(user_id),
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
        await self.bot.send_message(chat_id=self.chat_id, text=self.text)
