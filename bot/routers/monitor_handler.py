from aiogram import Router, F
from aiogram.types import Message

from bot.api.fine import Fine
from bot.api.helper.text import text_from_message
from bot.api.monitor.reshoot import reshoot
from bot.api.monitor.sharovar import sharovarshina
from bot.filter.filter import ENRMessage
from db.mongo.bot_settings import update_bot_settings, GetBotConstActivity
from db.mongo.users import update_user_activity, UserUpdateStatus, GetUserActivity

router = Router()


@router.message(ENRMessage())
async def router_text_handler(message: Message):
    active = update_bot_settings(GetBotConstActivity())
    if active:
        fine = Fine(message)
        text = await text_from_message(message)
        is_reshoot = await reshoot(text)
        if is_reshoot:
            await fine.issue("Нарушенние конституции ЕНР")
            return
        is_sharovarshina = sharovarshina(text)
        if is_sharovarshina:
            await fine.issue("Нарушенние конституции ЕНР")
            return
    else:
        print("Проверка отключена")
