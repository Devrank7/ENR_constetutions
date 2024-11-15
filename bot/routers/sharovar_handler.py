from aiogram import Router
from aiogram.enums import ChatType
from aiogram.filters import Command
from aiogram.types import Message, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()


@router.message(Command("sharovarshina"))
async def sharovarshina(message: Message):
    builder = InlineKeyboardBuilder()
    if message.chat.type == ChatType.PRIVATE:
        builder.button(text="Что такое ШАРОВАРЩИНА?🤔", web_app=WebAppInfo(
            url='https://www.rbc.ua/ukr/styler/shcho-take-sharovarshchina-abo-k-srsr-spaplyuzhiv-1669719773.html'
        ))
    else:
        builder.button(text="Что такое ШАРОВАРЩИНА?🤔",
                       url='https://www.rbc.ua/ukr/styler/shcho-take-sharovarshchina-abo-k-srsr-spaplyuzhiv-1669719773.html')
    await message.answer("Что такое ШІРІВІРЩІНА?", reply_markup=builder.as_markup())
