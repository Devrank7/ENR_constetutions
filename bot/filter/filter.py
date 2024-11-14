from typing import Any, Union, Dict

from aiogram.enums import ContentType
from aiogram.filters import Filter
from aiogram.types import Message


class ENRMessage(Filter):
    def __init__(self):
        super().__init__()

    async def __call__(self, message: Message) -> bool:
        return message.content_type in [ContentType.TEXT, ContentType.VOICE, ContentType.VIDEO_NOTE]
