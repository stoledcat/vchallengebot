from random import choice

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

from lexicon.lexicon import LEXICON, approved, not_approved

# инициализировать роутер уровня модуля
router = Router()


# выписаться из челленджа /sign_out
@router.message(Command(commands="sign_out"))
async def process_check_out_command(message: Message):
    # print(message.model_dump_json(indent=4, exclude_none=True))
    await message.reply(text=LEXICON["sign_out"])


# видео заметки
@router.message(F.video_note)
async def process_sent_voice(message: Message):
    if message.video_note.duration > 59:
        # print(message.model_dump_json(indent=4, exclude_none=True))
        await message.reply(text=choice(approved))
    else:
        await message.reply(text=choice(not_approved))
