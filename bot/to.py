from abc import ABC, abstractmethod

from aiogram import Bot
from aiogram.exceptions import TelegramAPIError
from aiogram.types import Message, ChatPermissions
from telethon.types import Chat
from telethon.tl.functions.channels import LeaveChannelRequest, InviteToChannelRequest
from telethon.tl.functions.messages import AddChatUserRequest, DeleteChatUserRequest

from bot.exception.exc import ArgsException, NoChatException
from bot.util.util import to_json
from telethon.tl.types import Message as TelethonMessage, InputPeerChat, InputPeerChannel, Channel

from client.client import get_client
from client.utils import check_auth


class MessageInfo:
    def __init__(self, date, message_id, text):
        self.date = date
        self.message_id = message_id
        self.text = text


async def get_history(bot: Bot, chat_id: int, limit: int = 100) -> list[MessageInfo]:
    return []


def get_param_or_raise(param: str, json_loader: dict):
    user_phone = json_loader.get(param)
    if not user_phone:
        raise ArgsException("No user_phone in json_loader")
    return user_phone


class To(ABC):
    def __init__(self, message: Message):
        self.message = message

    @abstractmethod
    async def send(self):
        raise NotImplementedError


class ToChat(To):
    async def check_chat(self, chat_id):
        try:
            chat = await self.bot.get_chat(chat_id)
            print("chat title:", chat.title)
        except Exception as e:
            raise NoChatException(e)

    def __init__(self, message: Message, json_loader: str):
        super().__init__(message)
        self.json_dict = to_json(json_loader)
        chat_id = self.json_dict.get("chat_id")
        if not chat_id:
            raise ArgsException("No chat_id in json_loader")
        self.chat_id = int(chat_id)
        text = self.json_dict.get("text")
        if not text:
            raise ArgsException("No text in json_loader")
        self.text = text
        self.bot = message.bot

    async def send(self):
        await self.check_chat(self.chat_id)
        reply_id = self.json_dict.get("reply_id")
        if reply_id:
            await self.bot.send_message(self.chat_id, self.text, reply_to_message_id=reply_id)
        else:
            await self.bot.send_message(chat_id=self.chat_id, text=self.text)


class ToChatUnban(ToChat):

    def __init__(self, message: Message, json_loader: str):
        super().__init__(message, json_loader)

    async def send(self):
        await self.check_chat(self.chat_id)
        user_id = self.json_dict.get("user_id")
        await self.bot.restrict_chat_member(
            chat_id=self.chat_id,
            user_id=int(user_id),
            permissions=ChatPermissions(
                can_send_messages=True,
                can_send_photos=True,
                can_send_voice=True,
                can_send_polls=True,
                can_send_documents=True,
                can_send_audios=True,
                can_send_videos=True,
                can_invite_users=True,
                can_pin_messages=True,
                can_send_other_messages=True,
                can_send_video_notes=True,
                can_send_voice_notes=True
            ),
        )
        await self.bot.send_message(chat_id=self.chat_id, text=self.text)


class ToAddUserAfterInsertTextAndAfterDeleteUserFromChat(ToChat):

    async def __add_to_chat(self, client):
        user = get_param_or_raise("username", self.json_dict)
        try:
            user_to_add = await client.get_entity(user)
            chat = await client.get_entity(self.chat_id)
            print("Type: ", type(chat))
            if isinstance(chat, Chat):
                await client(AddChatUserRequest(
                    chat_id=chat.id,
                    user_id=user_to_add,
                    fwd_limit=10
                ))
                print(f"Пользователь {user_to_add} добавлен в группу {chat.title}")
            elif isinstance(chat, Channel):
                await client(InviteToChannelRequest(
                    channel=chat,
                    users=[user_to_add]
                ))
                print(f"Пользователь {user_to_add} добавлен в канал/супергруппу {chat.title}")
        except Exception as e:
            print(f"Ошибка добавления пользователя: {e}")

    async def __leave_group(self, client):
        group = await client.get_entity(self.chat_id)
        if isinstance(group, Chat):
            await client(DeleteChatUserRequest(chat_id=group.id, user_id='me'))
        elif isinstance(group, Channel):
            await client(LeaveChannelRequest(channel=group))

    async def __connect_to_user_send(self):
        user = get_param_or_raise("user_other_phone", self.json_dict)
        telethon_client = get_client(f'session_{user}')
        try:
            telethon_client = await check_auth(telethon_client, self.message)
            await telethon_client.send_message(self.chat_id, self.text)
            await self.__leave_group(client=telethon_client)
        finally:
            await telethon_client.disconnect()

    async def send(self):
        await self.check_chat(self.chat_id)
        user_phone = get_param_or_raise("user_phone", self.json_dict)
        telethon_client = get_client(f'session_{user_phone}')
        try:
            telethon_client = await check_auth(telethon_client, self.message)
            await self.__add_to_chat(telethon_client)
            await self.__connect_to_user_send()
        finally:
            await telethon_client.disconnect()
