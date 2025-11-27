import asyncio
from datetime import datetime
from random import choice

import aiosqlite
from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from config import config
from config.config import DATABASE
from handlers.delete_message import delete_message_delayed as dm
from lexicon.lexicon import LEXICON, already_started, start

# инициализировать роутер уровня модуля
router = Router()


# Этот хэндлер будет срабатывать на команду "/start"
@router.message(CommandStart())
async def process_start_command(message: Message):
    date = datetime.now()
    iso_date = date.strftime("%Y-%m-%d %H:%M:%S")
    try:
        async with aiosqlite.connect(DATABASE) as db:
            user = message.from_user
            user_id = user.id
            # Проверить, есть ли пользователь в базе данных
            async with db.execute(
                "SELECT is_member FROM users WHERE user_id = ?", (user_id,)
            ) as cursor:
                row = await cursor.fetchone()

            if not row:
                await db.execute(
                    """
                    INSERT INTO users (
                        user_id,
                        username,
                        first_name,
                        last_name,
                        joined_at,
                        left_at,
                        is_member
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        user.id,
                        user.username,
                        user.first_name,
                        user.last_name,
                        iso_date,
                        None,
                        1,
                    ),
                )
                await db.commit()
                sent_message = await message.reply(text=choice(start))
            elif row[0] == 0:
                await db.execute(
                    """
                    UPDATE users
                    SET joined_at = ?, is_member = ?
                    WHERE user_id = ?
                    """,
                    (iso_date, 1, user.id),
                )
                await db.commit()
                sent_message = await message.reply(text=choice(start))
            else:
                sent_message = await message.reply(text=choice(already_started))

# удалить сообщение пользователя и ответ бота
            await dm(sent_message, config.DELAY_START_MESSAGE)
            await message.delete()
    except aiosqlite.IntegrityError as e:
# Логировать ошибку или информировать пользователя
        print(f"Integrity error: {e}")
        await message.reply(text=LEXICON["error"])


# Этот хэндлер будет срабатывать на команду "/help"
@router.message(Command(commands="help"))
async def process_help_command(message: Message):
    sent_message = await message.reply(text=LEXICON["/help"])
    await dm(sent_message, config.DELAY_HELP_MESSAGE)
    await message.delete()
