from html import escape

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message
from telethon import errors

from bot.states.states import AuthStates, HistoryStates, LogoutState
from client.client import get_client

router = Router()
phone_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Отправить номер телефона", request_contact=True)]
], resize_keyboard=True)


@router.message(Command('login'))
async def start_command(message: Message, state: FSMContext):
    await message.answer("Привет! Для авторизации введите номер телефона:", reply_markup=phone_keyboard)
    await state.set_state(AuthStates.waiting_for_phone)


@router.message(AuthStates.waiting_for_phone)
async def get_phone(message: Message, state: FSMContext):
    phone = message.contact.phone_number if message.contact else message.text
    telethon_client = get_client(f'session_{phone}')
    await state.update_data(phone=phone)
    await telethon_client.connect()
    if not await telethon_client.is_user_authorized():
        try:
            code = await telethon_client.send_code_request(phone)
            code_hash = code.phone_code_hash
            await state.update_data(code_hash=code_hash)
            await message.answer("Введите код из Telegram:")
            await state.set_state(AuthStates.waiting_for_code)
        except Exception as e:
            await message.answer(f"Ошибка при отправке кода: {e}")
            await telethon_client.disconnect()
            await state.clear()
    else:
        await message.answer("Вы уже авторизованы!")
        await state.clear()


@router.message(AuthStates.waiting_for_code)
async def get_code(message: Message, state: FSMContext):
    code = int(message.text)
    user_data = await state.get_data()
    phone = user_data.get("phone")
    code_hash = user_data.get("code_hash")
    telethon_client = get_client(f'session_{phone}')
    if not telethon_client.is_connected():
        await telethon_client.connect()
    try:
        await telethon_client.sign_in(phone, code, phone_code_hash=code_hash)
        await message.answer("Авторизация успешна!")
        await state.clear()
    except Exception as e:
        if isinstance(e, errors.SessionPasswordNeededError):
            await message.answer("Необходим пароль для двухфакторной аутентификации. Введите пароль:")
            await state.set_state(AuthStates.waiting_for_password)
        else:
            await message.answer(f"Ошибка при вводе кода: {e}")
            await telethon_client.disconnect()
            await state.clear()


@router.message(AuthStates.waiting_for_password)
async def get_password(message: Message, state: FSMContext):
    password = message.text
    user_data = await state.get_data()
    phone = user_data.get("phone")
    telethon_client = get_client(f'session_{phone}')
    if not telethon_client.is_connected():
        await telethon_client.connect()
    try:
        await telethon_client.sign_in(phone, password=password)
        await message.answer("Авторизация с 2FA завершена успешно!")
        await state.clear()
    except Exception as e:
        await message.answer(f"Ошибка авторизации: {e}")
    finally:
        await state.clear()


@router.message(Command("history"))
async def history(message: Message, state: FSMContext):
    await message.answer("Введите номер аккаунта на котором вы логинились!!")
    await state.set_state(HistoryStates.waiting_for_phone)


@router.message(HistoryStates.waiting_for_phone)
async def get_history(message: Message, state: FSMContext):
    phone = message.text
    telethon_client = get_client(f'session_{phone}')
    try:
        if not telethon_client.is_connected():
            await telethon_client.connect()
        if not await telethon_client.is_user_authorized():
            await message.answer("Вы не авторизованы. Сначала выполните авторизацию через /login.")
            return
        await state.update_data(phone=phone)
        await state.set_state(HistoryStates.waiting_for_chat_id)
        await message.answer("Введите chat id")
    finally:
        await telethon_client.disconnect()


@router.message(HistoryStates.waiting_for_chat_id)
async def get_chat_history(message: Message, state: FSMContext):
    user_data = await state.get_data()
    phone = user_data.get("phone")
    telethon_client = get_client(f'session_{phone}')
    try:
        if not telethon_client.is_connected():
            await telethon_client.connect()
        if not await telethon_client.is_user_authorized():
            await message.answer("Вы не авторизованы. Сначала выполните авторизацию через /login.")
            return
        chat_id = int(message.text)
        chat = await telethon_client.get_input_entity(chat_id)
        messages = await telethon_client.get_messages(chat, limit=100)
        if not messages:
            await message.answer("Сообщений в этом чате пока нет.")
            return
        history = "\n\n".join(
            [f"📩 <b>От:</b> {msg.sender_id}\n<b>Сообщение:</b> {msg.id}\n<b>Текст:</b> {escape(msg.text)}" for msg in
             messages
             if msg.text]
        )
        if len(history) > 4096:
            allowed_length = 4060
            while len(history) > allowed_length:
                history = history.rsplit('\n\n', 1)[0]
                history += "..."
        await message.answer(f"<b>Последние 100 сообщений:</b>\n\n{history}", parse_mode="HTML")
    finally:
        await telethon_client.disconnect()
        await state.clear()


@router.message(Command('logout'))
async def logout(message: Message, state: FSMContext):
    await message.answer("Введите номер телефона аккаунта")
    await state.set_state(LogoutState.waiting_for_phone)


@router.message(LogoutState.waiting_for_phone)
async def get_logout(message: Message, state: FSMContext):
    phone = message.text
    telethon_client = get_client(f'session_{phone}')
    try:
        if not telethon_client.is_connected():
            await telethon_client.connect()
        if not await telethon_client.is_user_authorized():
            await message.answer("Вы итак не авторизованы.")
            return
        await telethon_client.log_out()
        await message.answer('Вы вышли из системы!!!')
    finally:
        await telethon_client.disconnect()
        await state.clear()
