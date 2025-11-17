from random import choice

from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.methods import SendMessage
from aiogram.types import Message

from create_dp import dp
from lexicon.lexicon import LEXICON, start

# инициализировать роутер уровня модуля
router = Router()


# Этот хэндлер будет срабатывать на команду "/start"
@router.message(CommandStart())
async def process_start_command(message: Message):
    # print(message.model_dump_json(indent=4, exclude_none=True))
    await message.reply(text=choice(start))


# Этот хэндлер будет срабатывать на команду "/help"
@router.message(Command(commands="help"))
async def process_help_command(message: Message):
    # print(message.model_dump_json(indent=4, exclude_none=True))
    await message.reply(text=LEXICON["/help"])
