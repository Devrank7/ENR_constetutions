from aiogram.enums import ContentType
from aiogram.filters import Filter
from aiogram.types import Message


class ENRMessage(Filter):
    def __init__(self):
        super().__init__()

    async def __call__(self, message: Message) -> bool:
        print("FILTER")
        return message.content_type in [ContentType.PHOTO, ContentType.TEXT, ContentType.VOICE, ContentType.VIDEO_NOTE]
