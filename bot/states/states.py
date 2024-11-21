from aiogram.fsm.state import StatesGroup, State


class GPTMode(StatesGroup):
    active = State()


class GenerateState(StatesGroup):
    generate_prompt = State()


class AuthStates(StatesGroup):
    waiting_for_phone = State()
    waiting_for_code = State()
    waiting_for_password = State()


class LogoutState(StatesGroup):
    waiting_for_phone = State()


class HistoryStates(StatesGroup):
    waiting_for_phone = State()
    waiting_for_chat_id = State()
