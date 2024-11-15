from aiogram import Router
from aiogram.types import Message

from bot.api.fine import Fine
from bot.api.helper.text import text_from_message
from bot.api.monitor.reshoot import reshoot
from bot.api.monitor.sharovar import sharovarshina, Sharovarshina, FreeWordsOfENR
from bot.filter.filter import ENRMessage
from db.mongo.bot_settings import update_bot_settings, GetBotConstActivity

router = Router()


@router.message(ENRMessage())
async def router_text_handler(message: Message):
    active = update_bot_settings(GetBotConstActivity())
    if active:
        fine = Fine(message)
        text = await text_from_message(message)
        is_reshoot = reshoot(text, two_step=False)
        if is_reshoot:
            await fine.issue("Нарушенние конституции ЕНР")
            return
        is_sharovarshina, why_is_it_sharovarchina = Sharovarshina(text).check()
        if is_sharovarshina:
            await fine.issue(f"Нарушенние конституции ЕНР это Шароварщина. {why_is_it_sharovarchina}")
            return
        is_not_free_words = FreeWordsOfENR(text).check()

        print("Проверка окончена")
    else:
        print("Проверка отключена")
