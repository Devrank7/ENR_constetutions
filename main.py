import asyncio
import os

from aiogram import Bot, Dispatcher
from apscheduler.triggers.cron import CronTrigger
from dotenv import load_dotenv

from bot.routers import start_router, rules_router, bot_settings_handler, monitor_handler, sharovar_handler, \
    gpt_mode_handler
from sceduler.sceduler import scheduler
from sceduler.task import DistributedTask

load_dotenv()
os.environ["PATH"] += os.pathsep + r"F:\Downloads\ffmpeg\bin"
API_TOKEN = os.getenv('API_TOKEN')
bot = Bot(token=API_TOKEN)
dp = Dispatcher()
routers = [
    start_router.router,
    rules_router.router,
    bot_settings_handler.router,
    sharovar_handler.router,
    gpt_mode_handler.router,
    monitor_handler.router,
]


async def main():
    print("Start bot!")
    for router in routers:
        dp.include_router(router)
    distribute_task = DistributedTask(bot)
    scheduler.add_job(distribute_task.execute, CronTrigger(second='30'))
    scheduler.start()
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
