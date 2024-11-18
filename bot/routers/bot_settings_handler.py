from aiogram import Router, F
from aiogram.enums import ChatMemberStatus
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardMarkup, \
    KeyboardButton, ReplyKeyboardRemove

from bot.api.permision import my_permission_has
from db.mongo.bot_settings import update_bot_settings, GetBotConstActivity, UpdateBotChatsDistributes, \
    RemoveBotChatsDistributes, GetBotLock, UpdateBotLock, UpdateBotConstActivity

router = Router()


@router.message(Command("set"))
async def reshoot_handler(message: Message):
    action = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Yes", callback_data="a_y"),
         InlineKeyboardButton(text="No", callback_data="a_n")],
    ])
    await message.answer("Введите для активации или деактивации конституции: ", reply_markup=action)


@router.callback_query(F.data.startswith("a_"))
async def reshoot_handler(query: CallbackQuery):
    active = query.data.split("_")[1] == 'y'
    if active:
        has = await my_permission_has(query.message, [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR])
        if not has:
            await query.message.edit_text("Простите но даайте мне админку перед включение конституции!!!")
            return
    update_bot_settings(UpdateBotConstActivity(active))
    status = {"Включеный" if active else "Выключеный"}
    await query.answer(f"Статус активности конституции изменен на {status}", show_alert=True)
    await query.message.edit_text(f"Статус активности конституции изменен на {status}")


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


@router.message(Command("get_lock"))
async def get_lock(message: Message):
    lock = update_bot_settings(GetBotLock())
    has = await my_permission_has(message, [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR])
    warn = '' if has else ' Только дайте админку'
    text = f"Я не буду баннить только ругать🤬 пользователя который нарушил конституцию ЕНР {warn}" if lock else \
        f"Я буду баннить на некоторое время. И буду баннить за нарушения конституции📣 {warn}"
    await message.answer(text)


@router.message(Command("set_lock"))
async def set_lock(message: Message):
    reply_button = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="Сделать так чтобы я мог баннить за нарушение конституции")],
        [KeyboardButton(text="Сделать так чтобы я не мог баннить за нарушение конституции, а просто ругал")]
    ], resize_keyboard=True, one_time_keyboard=True)
    await message.answer("Выберете действие☑️", reply_markup=reply_button)


@router.message(F.text == "Сделать так чтобы я мог баннить за нарушение конституции")
async def set_lo(message: Message):
    has = await my_permission_has(message, [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR])
    update_bot_settings(UpdateBotLock(status=False))
    warn = '' if has else ' Только дайте админку!!!'
    await message.answer(f'Теперь я буду баннить за нарушение конституции🤠 {warn}', reply_markup=ReplyKeyboardRemove())


@router.message(F.text == "Сделать так чтобы я не мог баннить за нарушение конституции, а просто ругал")
async def set_loc(message: Message):
    update_bot_settings(UpdateBotLock(status=True))
    has = await my_permission_has(message, [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR])
    warn = '' if has else ' Только дайте админку!!!'
    await message.answer(f'Теперь я не могу баннить за нарушение конституции только критиковать😕 {warn}',
                         reply_markup=ReplyKeyboardRemove())
