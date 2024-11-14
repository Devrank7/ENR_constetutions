import re

from aiogram.types import Message

from bot.api.helper.recognize import recognize_type


async def text_from_message(message: Message) -> str:
    recognize_typ = recognize_type.get(message.content_type)
    text_reshoot = message.text
    if recognize_typ:
        voice_recognize = recognize_typ(message)
        text = await voice_recognize.recognize()
        print(text)
        text_reshoot = text
    return text_reshoot


def extract_text_from_angle_brackets(text: str) -> str:
    match = re.search(r'<(.*?)>', text)
    if match:
        return match.group(1)
    return "No"
