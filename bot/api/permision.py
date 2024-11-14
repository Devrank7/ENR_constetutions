import datetime

from aiogram import Bot
from aiogram.enums import ChatMemberStatus
from aiogram.types import Message, ChatPermissions

from bot.exception.exc import NotReplyException


async def my_permission_has(message: Message, permissions: list[ChatMemberStatus]):
    chat_id = message.chat.id
    bot_id = (await message.bot.get_me()).id
    bot_member = await message.bot.get_chat_member(chat_id, bot_id)
    return bot_member.status in permissions


async def ban(message: Message, minutes: int = 1, forever: bool = False):
    try:
        if forever:
            await message.bot.restrict_chat_member(
                chat_id=message.chat.id,
                user_id=message.reply_to_message.from_user.id,
                permissions=ChatPermissions(can_send_messages=False),
            )
            await message.answer(f"User {message.reply_to_message.from_user.first_name} has been ban.")
            return
        await message.bot.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=message.reply_to_message.from_user.id,
            permissions=ChatPermissions(can_send_messages=False),
            until_date=datetime.datetime.now() + datetime.timedelta(minutes=minutes)
        )
        await message.answer(
            f"User {message.reply_to_message.from_user.first_name} has been muted for {minutes} minutes.")
    except Exception as e:
        await message.answer(str(e))
