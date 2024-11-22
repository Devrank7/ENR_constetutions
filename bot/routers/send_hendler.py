import json
import traceback

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.api.helper.recognize import SegmentedVoiceRecognize
from bot.to import get_history, ToChat, ToChatUnban, ToAddUserAfterInsertTextAndAfterDeleteUserFromChat

router = Router()


@router.message(Command('his'))
async def send_history(message: Message):
    chat_id = message.text.split(' ')[1]
    messages = await get_history(bot=message.bot, chat_id=int(chat_id))
    message_ids = [m.message_id for m in messages]
    json_str = json.dumps({"messages": message_ids})
    await message.answer(json_str)


send_types = {
    "/to": ToChat,
    "/un": ToChatUnban,
    "/do": ToAddUserAfterInsertTextAndAfterDeleteUserFromChat
}


async def send(message: Message):
    try:
        json_loader = message.reply_to_message.text
        command = message.text[:3]
        await send_types.get(command)(message, json_loader).send()
        await message.answer("Я отслал сообщение в другой чат!!!")
    except Exception as e:
        traceback.print_exc()
        await message.answer("Какая то ошибочка. {}".format(e))


@router.message(Command("to"))
async def send_hendler(message: Message):
    await send(message)


@router.message(Command("un"))
async def send_unban(message: Message):
    await send(message)


@router.message(Command("down"))
async def send_down(message: Message):
    await send(message)


def words_dilimeters(text: str) -> list[int]:
    length = float(len(text) / 4000)
    to_int = int(length)
    remainder = length - to_int
    dilimiters = [(4000 * d) for d in range(to_int + 1)]
    dilimiters.append((dilimiters[-1] + int(4000 * remainder)))
    return dilimiters


@router.message(Command('reco'))
async def send_reco(message: Message):
    reply_message = message.reply_to_message
    if not reply_message:
        await message.answer('Закрипите сообщение')
        return
    texts = await SegmentedVoiceRecognize(reply_message).recognize()
    for text in texts:
        await message.answer(text)
