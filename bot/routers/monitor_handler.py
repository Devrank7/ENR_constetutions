from aiogram import Router, F
from aiogram.types import Message

from bot.api.helper.text import text_from_message
from bot.api.monitor.reshoot import reshoot
from bot.filter.filter import ENRMessage
from db.mongo.service import update_bot_settings, GetBotConstActivity

router = Router()


@router.message(ENRMessage())
async def router_text_handler(message: Message):
    active = update_bot_settings(GetBotConstActivity())
    if active:
        text = await text_from_message(message)
        is_reshoot = await reshoot(text)
        if is_reshoot:
            await message.answer("Нарушение конституции ЕНР")
            return
        is_sharovarshina = True
    else:
        print("Проверка отключена")
