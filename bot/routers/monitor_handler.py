from aiogram import Router
from aiogram.types import Message

from bot.api.fine import Fine
from bot.api.helper.text import text_from_message
from bot.api.monitor.issue import issue_fine_for_user_if_has
from bot.api.my import UpdateMessage
from bot.filter.filter import ENRMessage
from db.mongo.bot_settings import update_bot_settings, GetBotConstActivity

router = Router()


@router.message(ENRMessage())
async def router_text_handler(message: Message):
    update = UpdateMessage(message)
    result = await update.update()
    if result:
        return
    active = update_bot_settings(GetBotConstActivity())
    if active:
        fine = Fine(message)
        text = await text_from_message(message)
        await issue_fine_for_user_if_has(fine, text)
        print("Проверка окончена")
    else:
        print("Проверка отключена")
