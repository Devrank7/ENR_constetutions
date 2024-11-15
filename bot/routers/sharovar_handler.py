from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()


@router.message(Command("sharovarshina"))
async def sharovarshina(message: Message):
    markup = InlineKeyboardBuilder()
    markup.button(text="Что такое шароваршина?🤔",
                  web_app=WebAppInfo(
                      url=
                      'https://www.rbc.ua/ukr/styler/shcho-take-sharovarshchina-abo-k-srsr-spaplyuzhiv-1669719773.html')
                  )
    await message.answer("Что такое ШІРІВІРЩІНА?", reply_markup=markup.as_markup())
