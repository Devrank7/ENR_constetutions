from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.api.permision import ReplyBan, ReplyUnban
from bot.middleware.admin_middleware import AdminMiddleware

router = Router()
router.message.middleware(AdminMiddleware())


@router.message(Command('mute'))
async def mute(message: Message):
    try:
        reply_ban = ReplyBan(message=message, minutes=int(message.text.split(' ')[-1]))
        await reply_ban.restrict()
    except ValueError as e:
        await message.answer(str(e))


@router.message(Command('unban'))
async def unmute(message: Message):
    reply_unban = ReplyUnban(message)
    await reply_unban.restrict()


@router.message(Command('ban'))
async def bans(message: Message):
    reply_ban = ReplyBan(message=message, forever=True)
    await reply_ban.restrict()
