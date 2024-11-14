from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from db.mongo.service import update_bot_settings, UpdateBotChatsDistributes, RemoveBotChatsDistributes

router = Router()


@router.message(Command("distribute"))
async def distribute(message: Message):
    distribute_action = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Yes", callback_data="d_yes"),
         InlineKeyboardButton(text="No", callback_data="d_no")],
    ])
    await message.answer("Distribute action", reply_markup=distribute_action)


@router.callback_query(F.data.startswith("d_"))
async def d_callback(query: CallbackQuery):
    status = query.data.split("_")[1].lower() == "yes"
    await query.answer()
    if status:
        update_bot_settings(UpdateBotChatsDistributes(chat_id=query.chat.id))
        await query.message.edit_text("Add chat in")
    else:
        update_bot_settings(RemoveBotChatsDistributes(chat_id=query.chat.id))
        await query.message.edit_text("Remove chat from")

