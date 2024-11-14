from aiogram.fsm.state import StatesGroup, State


class Constitutions(StatesGroup):
    active = State()


class GPTMode(StatesGroup):
    active = State()
