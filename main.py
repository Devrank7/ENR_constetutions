import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from apscheduler.events import EVENT_JOB_ERROR
from apscheduler.triggers.cron import CronTrigger
from dotenv import load_dotenv

from bot.routers import start_router, rules_router, bot_settings_handler, monitor_handler, sharovar_handler, \
    gpt_mode_handler, change_router, ebenya_router, send_hendler, client_routers
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
    change_router.router,
    ebenya_router.router,
    send_hendler.router,
    client_routers.router,
    monitor_handler.router,
]


def job_error_listener(event):
    if event.exception:
        logging.error(f"Ошибка в задаче: {event.job_id}", exc_info=event.exception)


async def main():
    print("Start bot!")
    for router in routers:
        dp.include_router(router)
    weekend_task = DistributedTask(bot, "Выходные поздравляю мы это выдержали!!!😎😎😎")
    start_week_task = DistributedTask(bot, "Опять уроки НЕЕЕЕТ😭😭😭😭😭")
    holiday_winter = DistributedTask(bot, "Зимние Каникулы УРАААААА!!!🥳🥳🥳🥳🥳🥳🥳🥳")
    holiday_spring = DistributedTask(bot, "Весение Каникулы УРАААААА!!!🥳🥳🥳🥳🥳🥳🥳🥳")
    holiday_summer = DistributedTask(bot,
                                     "Это свершилось ЛЕТНИЕ Каникулы УРАААААА!!!🥳🥳🥳🥳🥳🥳🥳🥳🥳🥳🥳🥳🥳🥳🥳🥳🥳🥳🥳🥳🥳🥳🥳🥳🥳🥳🥳🥳🥳🥳")
    holiday_autumn = DistributedTask(bot, "Осение Каникулы УРАААААА!!!🥳🥳🥳🥳🥳🥳🥳🥳")
    refresh_fines_task = RefreshFineTask(bot)
    scheduler.add_job(weekend_task.execute, CronTrigger(day_of_week='5', hour='14'))
    scheduler.add_job(start_week_task.execute, CronTrigger(day_of_week='1', hour='8'))
    scheduler.add_job(refresh_fines_task.execute, CronTrigger(day_of_week='0', hour='12'))  # Воскресенье
    scheduler.add_job(holiday_autumn.execute, CronTrigger(month='10', day='27', hour='14'))
    scheduler.add_job(holiday_winter.execute, CronTrigger(month='12', day='27', hour='14'))
    scheduler.add_job(holiday_spring.execute, CronTrigger(month='3', day='30', hour='14'))
    scheduler.add_job(holiday_summer.execute, CronTrigger(month='5', day='31'))
    scheduler.add_listener(job_error_listener, EVENT_JOB_ERROR)
    scheduler.start()
    await bot.delete_webhook()
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
