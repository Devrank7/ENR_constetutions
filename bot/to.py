from abc import ABC, abstractmethod

from aiogram import Bot
from aiogram.exceptions import TelegramAPIError
from aiogram.types import Message

from bot.exception.exc import ArgsException, NoChatException
from bot.util.util import to_json


async def get_history(bot: Bot, chat_id: int, limit: int = 100) -> list[Message]:
    messages = []
    try:
        updates = await bot.get_updates(limit=limit)
        for update in updates:
            if update.message and update.message.chat.id == chat_id:
                messages.append(update.message)
    except TelegramAPIError as e:
        print(f"Ошибка API Telegram: {e}")
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

    def __init__(self, message: Message, json_loader: str):
        super().__init__(message)
        self.json_dict = to_json(json_loader)
        chat_id = self.json_dict.get("chat_id")
        text = self.json_dict.get("text")
        if not chat_id:
            raise ArgsException("No chat_id in json_loader")
        if not text:
            raise ArgsException("No text in json_loader")
        self.chat_id = int(chat_id)
        self.text = text

    async def send(self):
        await self.check_chat(self.chat_id)
        reply_id = self.json_dict.get("reply_id")
        if reply_id:
            await self.message.bot.send_message(self.chat_id, self.text, reply_to_message_id=reply_id)
        else:
            await self.message.bot.send_message(chat_id=self.chat_id, text=self.text)
