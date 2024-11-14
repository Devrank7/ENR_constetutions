import datetime

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, ChatPermissions

from bot.api.permision import ban
from bot.exception.exc import NotReplyException
from bot.middleware.admin_middleware import AdminMiddleware

router = Router()
router.message.middleware(AdminMiddleware())


@router.message(Command('mute'))
async def mute(message: Message):
    try:
        if message.reply_to_message is None:
            raise NotReplyException
        time_minutes = int(message.text.split(' ')[-1])
        if time_minutes <= 0 or time_minutes > 3600:
            raise ValueError
        await ban(message, minutes=time_minutes)
    except ValueError:
        await message.answer("Enter number of minutes from 1 to 3600")
    except NotReplyException:
        await message.answer("Reply to a message to mute")
    except Exception as e:
        await message.answer(str(e))


@router.message(Command('unban'))
async def unmute(message: Message):
    try:
        if message.reply_to_message is None:
            raise NotReplyException
        user_reply_id = message.reply_to_message.from_user.id
        await message.bot.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=user_reply_id,
            permissions=ChatPermissions(can_send_messages=True),
        )
        await message.answer(f"Unmuted user {message.reply_to_message.from_user.first_name}")
    except NotReplyException:
        await message.answer("Reply to a message to mute")
    except Exception as e:
        await message.answer(str(e))


@router.message(Command('ban'))
async def bans(message: Message):
    try:
        if message.reply_to_message is None:
            raise NotReplyException
        await ban(message, forever=True)
    except NotReplyException:
        await message.answer("Reply to a message to mute")
    except Exception as e:
        await message.answer(str(e))
