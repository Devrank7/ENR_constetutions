import asyncio
import io
import uuid

import aiohttp
from aiogram import Router, F
from aiogram.enums import ChatAction, ChatMemberStatus
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InputFile, FSInputFile, URLInputFile

from bot.api.ai.ai import ChatGPT, generate, FluxGPT
from bot.api.ai.models import GPTModels, FluxModels
from bot.api.permision import my_permission_has
from bot.states.states import GPTMode, GenerateState
from bot.util.keyboard import as_keyboard_markup, GPTModelsKeyboardMarkup, FluxModelsKeyboardMarkup

router = Router()


@router.message(Command("gpt"))
async def gpt(message: Message):
    markup = as_keyboard_markup(GPTModelsKeyboardMarkup())
    await message.answer("Выберете модель гпт (генеративного предобученого трансформера): ", reply_markup=markup)


@router.callback_query(F.data.startswith("gpt_"))
async def gpt_callback(query: CallbackQuery, state: FSMContext):
    model = query.data.split("_")[1]
    has = await my_permission_has(query.message, [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR])
    if not has:
        await query.message.edit_text("Если хочешь гпт мод то сделай меня админом!!!!!")
        return
    await state.update_data(model=model)
    await query.answer(f"ГПТ мод активирован👾 Задавайте вопросы. Моделька {model} активированна!")
    await state.set_state(GPTMode.active)
    await query.message.edit_text(
        f"ГПТ мод активирован👾 Задавайте вопросы. Моделька {model} активированна! Чтобы выйти из мода введи 'Q'")


@router.message(GPTMode.active)
async def gpt_mode(message: Message, state: FSMContext):
    if message.text.lower() == "q":
        await message.answer("Выход из гпт режима...")
        await state.clear()
        return
    data = await state.get_data()
    model = GPTModels(data["model"])

    async def send_typing():
        while not stop_typing.is_set():
            await message.bot.send_chat_action(message.chat.id, ChatAction.TYPING)
            await asyncio.sleep(5)

    stop_typing = asyncio.Event()
    typing_task = asyncio.create_task(send_typing())
    try:
        response = await generate(ChatGPT(prompt=message.text, model=model))
    finally:
        stop_typing.set()
        await typing_task
    await message.answer(response)
    await state.set_state(GPTMode.active)


@router.message(Command("generate"))
async def gpt_generate(message: Message):
    markup = as_keyboard_markup(FluxModelsKeyboardMarkup())
    await message.answer("Выберете модель FLUX для генерации картинок🐰 ", reply_markup=markup)


@router.callback_query(F.data.startswith("flux_"))
async def gpt_callback(query: CallbackQuery, state: FSMContext):
    model = query.data.split("_")[1]
    if not await my_permission_has(query.message, [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]):
        await query.message.edit_text("Если хочешь FLUX мод для генирации картинок то сделай меня админом!!!!!")
        return
    await state.update_data(model=model)
    await state.set_state(GenerateState.generate_prompt)
    await query.answer(f"Задавайте я {model} мне запросики на АНГЛИЙСКОМ и я сгенерирую красивую картинку🥰", show_alert=True)
    await query.message.edit_text(f"Задавайте я {model} мне запросики на АНГЛИЙСКОМ и я сгенерирую красивую картинку🥰")


async def download_image(url: str, file_path: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                with open(file_path, 'wb') as f:
                    f.write(await response.read())
            else:
                raise Exception(f"Failed to download image. Status code: {response.status}")


@router.message(GenerateState.generate_prompt)
async def gpt_generate_prompt(message: Message, state: FSMContext):
    if message.text.lower() == "q":
        await message.answer("Выход из FLUX режима генирации изображений...")
        await state.clear()
        return
    data = await state.get_data()
    model = FluxModels(data["model"])

    async def send_typing():
        while not stop_upload.is_set():
            await message.bot.send_chat_action(message.chat.id, ChatAction.UPLOAD_PHOTO)
            await asyncio.sleep(5)

    stop_upload = asyncio.Event()
    upload_task = asyncio.create_task(send_typing())
    try:
        url = await generate(FluxGPT(prompt=message.text, models=model))
    finally:
        stop_upload.set()
        await upload_task
    print("URL = ", url)
    file = URLInputFile(url=url)
    await message.answer_photo(photo=file, caption=message.text)
