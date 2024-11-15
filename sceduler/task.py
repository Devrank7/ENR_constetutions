from abc import ABC, abstractmethod

from aiogram import Bot

from db.mongo.bot_settings import update_bot_settings, GetBotChatsDistributes

from db.mongo.users import update_user_activity, ResetAllUserActivity


class Task(ABC):
    @abstractmethod
    async def execute(self):
        raise NotImplementedError


class DistributedTask(Task):

    def __init__(self, bot: Bot, text: str):
        self.bot = bot
        self.text = text

    async def execute(self):
        chats = update_bot_settings(GetBotChatsDistributes())
        print('c')
        for chat in chats:
            await self.bot.send_message(chat_id=chat, text=self.text)


class RefreshFineTask(Task):
    def __init__(self, bot: Bot):
        self.bot = bot

    async def execute(self):
        update_user_activity(ResetAllUserActivity())
        await DistributedTask(self.bot, "Все замечания за штрафи обнулены теперь можете спать спокойно🥰").execute()
