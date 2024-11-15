from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.api.ai.ai import ChatGPT, generate
from bot.api.ai.models import GPTModels
from bot.states.states import GPTMode
from bot.util.keyboard import as_keyboard_markup, GPTModelsKeyboardMarkup

router = Router()


@router.message(Command("gpt"))
async def gpt(message: Message):
    markup = as_keyboard_markup(GPTModelsKeyboardMarkup())
    await message.answer("Choose role: ", reply_markup=markup)


@router.callback_query(F.data.startswith("gpt_"))
async def gpt_callback(query: CallbackQuery, state: FSMContext):
    model = query.data.split("_")[1]
    await state.update_data(model=model)
    await query.answer(f"GPT mode activate. Model {model} activate!")
    await state.set_state(GPTMode.active)
    await query.message.edit_text(f"GPT mode activate. Model {model} activate! Leave mode type Q")


@router.message(GPTMode.active)
async def gpt_mode(message: Message, state: FSMContext):
    if message.text.lower() == "q":
        await message.answer("Quitting...")
        await state.clear()
        return
    data = await state.get_data()
    model = GPTModels(data["model"])
    response = generate(ChatGPT(prompt=message.text, model=model))
    await message.answer(response)
    await state.set_state(GPTMode.active)
