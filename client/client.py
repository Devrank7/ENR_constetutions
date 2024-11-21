import os

from dotenv import load_dotenv
from telethon import TelegramClient

load_dotenv()
API_ID = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')

clients = {}


def get_client(session: str) -> TelegramClient:
    client = clients.get(session)
    print("client: ", client)
    if client is None:
        client = TelegramClient(session, API_ID, API_HASH)
        clients[session] = client
    return client
