from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from bot.states.states import Constitutions
from db.mongo.bot_settings import update_bot_settings, GetBotConstActivity, UpdateBotChatsDistributes, \
    RemoveBotChatsDistributes

router = Router()


@router.message(Command("set"))
async def reshoot_handler(message: Message, state: FSMContext):
    await state.set_state(Constitutions.active)
    await message.answer("Введите для активации или деактивации конституции Y/n")


@router.message(Constitutions.active)
async def reshoot_handler(message: Message, state: FSMContext):
    active = message.text.lower() == 'y'
    data = await state.update_data(active=active)
    update_bot_settings(data['active'])
    await state.clear()
    await message.answer(f"Статус активности конституции изменен на {"Включеный" if active else "Выключеный"}")


@router.message(Command("get"))
async def reshoot_handler(message: Message):
    activity = update_bot_settings(GetBotConstActivity())
    await message.answer(f"Статус активности конституции {activity}")


@router.message(Command("distribute"))
async def distribute(message: Message):
    distribute_action = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Yes", callback_data="d_yes"),
         InlineKeyboardButton(text="No", callback_data="d_no")],
    ])
    await message.answer("Уведомлять о снятие штрафов пользователей, выходных, каникулах🤗.",
                         reply_markup=distribute_action)


@router.callback_query(F.data.startswith("d_"))
async def d_callback(query: CallbackQuery):
    status = query.data.split("_")[1].lower() == "yes"
    await query.answer()
    if status:
        update_bot_settings(UpdateBotChatsDistributes(chat_id=query.message.chat.id))
        await query.message.edit_text("Ваш чат добавился в уведомляторы")
    else:
        update_bot_settings(RemoveBotChatsDistributes(chat_id=query.message.chat.id))
        await query.message.edit_text("Ваш чат удалился из уведомляторах")
