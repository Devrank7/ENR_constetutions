from aiogram import Router, F
from aiogram.types import Message

from bot.api.monitor.reshoot import reshoot
from bot.filter.filter import ENRMessage
from db.mongo.service import update_bot_settings, GetBotConstActivity

router = Router()


@router.message(ENRMessage())
async def router_text_handler(message: Message):
    active = update_bot_settings(GetBotConstActivity())
    if active:
        is_reshoot = await reshoot(message)
        if is_reshoot:
            await message.answer("Нарушение конституции ЕНР")
    else:
        print("Проверка отключена")
