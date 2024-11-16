from aiogram.fsm.state import StatesGroup, State


class GPTMode(StatesGroup):
    active = State()
