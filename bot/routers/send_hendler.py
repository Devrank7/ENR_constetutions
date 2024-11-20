import json
import traceback

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.api.helper.recognize import SegmentedVoiceRecognize
from bot.api.helper.text import text_from_message
from bot.to import get_history, ToChat

router = Router()


@router.message(Command('history'))
async def send_history(message: Message):
    chat_id = message.text.split(' ')[1]
    messages = await get_history(bot=message.bot, chat_id=int(chat_id))
    message_ids = [m.message_id for m in messages]
    json_str = json.dumps({"messages": message_ids})
    await message.answer(json_str)


@router.message(Command("to"))
async def send_hendler(message: Message):
    try:
        json_loader = message.reply_to_message.text
        await ToChat(message, json_loader).send()
        await message.answer("Я отслал сообщение в другой чат!!!")
    except Exception as e:
        traceback.print_exc()
        await message.answer("Какая то ошибочка. {}".format(e))


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
    texts = await SegmentedVoiceRecognize(message).recognize()
    for text in texts:
        await message.answer(text)
    # text = await text_from_message(reply_message)
    # dil = words_dilimeters(text)
    # for i, di in enumerate(dil):
    #     try:
    #         last_index = dil[i + 1]
    #     except IndexError:
    #         break
    #     t = text[dil[i]:last_index]
    #     await message.answer(t)
