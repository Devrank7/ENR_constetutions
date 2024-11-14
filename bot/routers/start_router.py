from aiogram import Router
from aiogram.enums import ChatMemberStatus
from aiogram.filters import CommandStart
from aiogram.types import Message

from bot.api.permision import my_permission_has

router = Router()


@router.message(CommandStart())
async def start_router(message: Message):
    has = await my_permission_has(message, [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR])
    warning = "I do not ban or mute users make me admin" if not has else ""
    await message.answer(f"Constitutions of ENR: {warning}")
