import asyncio
import os

from aiogram import Bot, Dispatcher
from apscheduler.triggers.cron import CronTrigger
from dotenv import load_dotenv

from bot.routers import start_router, rules_router, bot_settings_handler, monitor_handler, sharovar_handler, \
    gpt_mode_handler
from sceduler.sceduler import scheduler
from sceduler.task import DistributedTask, RefreshFineTask

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
    distribute_task = DistributedTask(bot, "Выходные поздравляю мы это выдержали!!!😎😎😎")
    distribute_task_bad = DistributedTask(bot, "Опять уроки НЕЕЕЕТ😭😭😭😭😭")
    holiday_winter = DistributedTask(bot, "Зимние Каникулы УРАААААА!!!🥳🥳🥳🥳🥳🥳🥳🥳")
    holiday_spring = DistributedTask(bot, "Весение Каникулы УРАААААА!!!🥳🥳🥳🥳🥳🥳🥳🥳")
    holiday_summer = DistributedTask(bot,
                                     "Это свершилось ЛЕТНИЕ Каникулы УРАААААА!!!🥳🥳🥳🥳🥳🥳🥳🥳🥳🥳🥳🥳🥳🥳🥳🥳🥳🥳🥳🥳🥳🥳🥳🥳🥳🥳🥳🥳🥳🥳")
    holiday_autumn = DistributedTask(bot, "Осение Каникулы УРАААААА!!!🥳🥳🥳🥳🥳🥳🥳🥳")
    refresh_fines_task = RefreshFineTask(bot)
    scheduler.add_job(distribute_task.execute, CronTrigger(second='30'))
    scheduler.add_job(distribute_task_bad.execute, CronTrigger(minute='30'))
    scheduler.add_job(refresh_fines_task.execute, CronTrigger(second='45'))
    scheduler.start()
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
