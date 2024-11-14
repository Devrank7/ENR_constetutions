from abc import ABC, abstractmethod

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.api.ai.models import GPTModels


class KeyboardsMarkup(ABC):
    @abstractmethod
    def as_keyboard_markup(self) -> InlineKeyboardMarkup:
        raise NotImplementedError


class GPTModelsKeyboardMarkup(KeyboardsMarkup):

    def __init__(self, callback_prefix: str = "gpt_", delimiter: int = 3):
        self.delimiter = delimiter
        self.callback_prefix = callback_prefix

    def as_keyboard_markup(self) -> InlineKeyboardMarkup:
        keyboard_builder = InlineKeyboardBuilder()
        for role in GPTModels:
            keyboard_builder.button(
                text=role.value,
                callback_data=f"{self.callback_prefix}{role.value}"
            )
        keyboard_builder.adjust(self.delimiter)
        return keyboard_builder.as_markup()


def as_keyboard_markup(keyboard: KeyboardsMarkup) -> InlineKeyboardMarkup:
    return keyboard.as_keyboard_markup()
