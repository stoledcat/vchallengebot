from datetime import datetime
from random import choice

import aiosqlite
from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from config import config
from config.config import DATABASE
from handlers.delete_message import delete_message_delayed as dm
from lexicon.lexicon import LEXICON, already_started, start, video_approved

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
            # проверить запись видео во временной таблице
            async with db.execute(
                "SELECT user_id, chat_id, created_at FROM pending_video_notes WHERE user_id = ? AND chat_id = ?",
                (user.id, message.chat.id),
            ) as check_pending:
                check_row = await check_pending.fetchone()

            # Проверить, является ли пользователь участником челленджа в чате, откуда был отправлен запрос
            async with db.execute(
                "SELECT user_id, chat_id FROM is_member WHERE user_id = ? AND chat_id = ? ",
                (
                    message.from_user.id,
                    message.chat.id,
                ),
            ) as cursor:
                row = await cursor.fetchone()
            if not row:
                # записать нового пользователя в базу данных
                await db.execute(
                    """
                    INSERT INTO users (
                        user_id,
                        username,
                        first_name,
                        last_name,
                        joined_at
                    ) VALUES (?, ?, ?, ?, ?)
                    """,
                    (user.id, user.username, user.first_name, user.last_name, iso_date),
                )
                # сопоставить user_id и chat_id в таблице is_member - фиксирование принятие участия в определенном чате
                await db.execute(
                    """
                    INSERT INTO is_member (
                    user_id,
                    chat_id,
                    username,
                    chat_title
                    ) VALUES (?, ?, ?, ?)
                    """,
                    (user.id, message.chat.id, (user.username or user.first_name), message.chat.title),
                )
                # записать чат в базу данных
                await db.execute(
                    """
                    INSERT INTO chats (
                    chat_id,
                    chat_title,
                    created_at
                    ) VALUES (?, ?, ?)
                    """,
                    (message.chat.id, message.chat.title, iso_date),
                )

                # записаь событие в events
                await db.execute(
                    "INSERT INTO events (chat_title, user_id, username, first_name, last_name, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                    (
                        message.chat.title,
                        user.id,
                        user.username,
                        user.first_name,
                        user.last_name,
                        iso_date or check_row[2],
                    ),
                )

                await db.commit()
                # удалить запись из временной
                if check_row:
                    await db.execute(
                        "DELETE FROM pending_video_notes WHERE user_id = ? AND chat_id = ?",
                        (
                            check_row[0],
                            check_row[1],
                        ),
                    )
                    await db.commit()
                    sent_message = await message.reply(text=choice(video_approved))
                    await dm(sent_message, config.DELAY_START_MESSAGE)
                else:
                    sent_message = await message.reply(text=choice(start))
            else:
                await db.commit()
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
