from datetime import datetime
from random import choice

import aiosqlite
from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from lexicon.lexicon import LEXICON, start, already_started

# инициализировать роутер уровня модуля
router = Router()


# Этот хэндлер будет срабатывать на команду "/start"
@router.message(CommandStart())
async def process_start_command(message: Message):
    date = datetime.now()
    formatted_datetime = date.strftime("%d.%m.%Y %H:%M:%S")
    try:
        async with aiosqlite.connect("app/vplanke.db") as db:
            user = message.from_user
            await db.execute(
                """
                INSERT INTO users (
                    user_id,
                    username,
                    first_name,
                    last_name,
                    joined_at,
                    left_at,
                    chat_id,
                    is_member
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    user.id,
                    user.username,
                    user.first_name,
                    user.last_name,
                    formatted_datetime,
                    None,
                    message.chat.id,
                    1,
                ),
            )
            await db.commit()
        await message.reply(text=choice(start))
    except aiosqlite.IntegrityError:
        await message.reply(text=choice(already_started))


# Этот хэндлер будет срабатывать на команду "/help"
@router.message(Command(commands="help"))
async def process_help_command(message: Message):
    await message.reply(text=LEXICON["/help"])
