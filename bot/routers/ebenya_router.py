from aiogram import Router
from aiogram.enums import ChatType
from aiogram.filters import Command
from aiogram.types import Message, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()


@router.message(Command('ebenya'))
async def ebenya_router(message: Message):
    builder = InlineKeyboardBuilder()
    if message.chat.type == ChatType.PRIVATE:
        builder.button(text="Я хочу попасть туда", web_app=WebAppInfo(
            url='https://ebenya.pp.ua/api/'
        ))
    else:
        builder.button(text="Я хочу попасть туда",
                       url='https://ebenya.pp.ua/api/')
    await message.answer("Ебеньвсое королевство!😎", reply_markup=builder.as_markup())
