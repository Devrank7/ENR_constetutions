from aiogram.types import Message
from telethon import TelegramClient

from bot.exception.exc import NoClientAuthorizedException


async def check_auth(client: TelegramClient, message: Message, text: str = "Вы не авторизованы."):
    if not client.is_connected():
        await client.connect()
    if not await client.is_user_authorized():
        await message.answer(text)
        raise NoClientAuthorizedException(text)
    return client
