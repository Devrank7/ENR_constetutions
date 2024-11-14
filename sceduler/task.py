from abc import ABC, abstractmethod

from aiogram import Bot

from db.mongo.service import update_bot_settings, GetBotChatsDistributes


class Task(ABC):
    @abstractmethod
    async def execute(self):
        raise NotImplementedError


class DistributedTask(Task):

    def __init__(self, bot: Bot):
        self.bot = bot

    async def execute(self):
        chats = update_bot_settings(GetBotChatsDistributes())
        print('c')
        for chat in chats:
            await self.bot.send_message(chat_id=chat, text="Weekend!!!")
