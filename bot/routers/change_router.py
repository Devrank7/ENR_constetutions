from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from db.mongo.bot_settings import update_bot_settings, AddChangesUsers, RemoveChangesUsers

router = Router()


@router.message(Command("anonim"))
async def mine(message: Message):
    update_bot_settings(AddChangesUsers(message.from_user.id))
    await message.reply("Теперь ты аномим!!!")


@router.message(Command("un_anonim"))
async def un_mine(message: Message):
    update_bot_settings(RemoveChangesUsers(message.from_user.id))
    await message.reply("Теперь ты не аноним!!!")
