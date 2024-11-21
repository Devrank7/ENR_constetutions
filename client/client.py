import os

from dotenv import load_dotenv
from telethon import TelegramClient

load_dotenv()
API_ID = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')


def get_client(session: str) -> TelegramClient:
    return TelegramClient(session, API_ID, API_HASH)
