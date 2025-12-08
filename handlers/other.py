import asyncio
from datetime import datetime
from random import choice

import aiosqlite
from aiogram import F, Router
from aiogram.filters import IS_MEMBER, IS_NOT_MEMBER, ChatMemberUpdatedFilter, Command
from aiogram.types import ChatMemberUpdated, Message

from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from config import config
from config.config import DATABASE, VIDEO_NOTE_DURATION
from handlers.delete_message import delete_message_delayed as dm
from lexicon.lexicon import LEXICON, approved, not_approved

# инициализировать роутер уровня модуля
router = Router()


class Reg(StatesGroup):
    # Состояние для ожидания ответа от пользователя
    waiting_for_response = State()


# Выписаться из челленджа /sign_out
@router.message(Command(commands="sign_out"))
async def process_check_out_command(message: Message):
    try:
        async with aiosqlite.connect(DATABASE) as db:
            user = message.from_user
            user_id = user.id
            async with db.execute(
                "SELECT user_id, chat_id FROM is_member WHERE user_id = ? AND chat_id = ? ",
                (
                    message.from_user.id,
                    message.chat.id,
                ),
            ) as cursor:
                row = await cursor.fetchone()
            if not row:
                sent_message = await message.reply(text=LEXICON["not_in_base"])
            else:
                await db.execute(
                    """DELETE FROM is_member WHERE user_id = ? AND chat_id = ?""",
                    (
                        int(message.from_user.id),
                        (int(message.chat.id)),
                    ),
                )

                await db.commit()
                sent_message = await message.reply(text=LEXICON["sign_out"])

            # удалить сообщение пользователя и ответ бота
            await dm(sent_message, config.DELAY_NOTIFY)
            await message.delete()

    except aiosqlite.IntegrityError as e:
        # Логировать ошибку или информировать пользователя
        print(f"Integrity error: {e}")
        sent_message = await message.reply(text=LEXICON["error"])
        await dm(sent_message, config.DELAY_ERROR_MESSAGE)


# Проверка видео заметок (кружочков)
@router.message(F.video_note)
async def process_sent_voice(message: Message):
    # user_id = user.id
    chat_id = message.chat.id
    chat_title = message.chat.title
    user_id = message.from_user.id
    username = message.from_user.username
    user_first_name = message.from_user.first_name
    user_last_name = message.from_user.last_name
    date = datetime.now()
    iso_date = date.strftime("%Y-%m-%d %H:%M:%S")

    # Проверить длительность видео заметки
    if message.video_note.duration > VIDEO_NOTE_DURATION:
        try: # Проверить, является ли пользователь участником челленджа
            async with aiosqlite.connect(DATABASE) as db:
                async with db.execute(
                    "SELECT user_id, chat_id FROM is_member WHERE user_id = ? AND chat_id = ?",
                    (user_id, chat_id,),
                ) as member_cursor:
                    is_member = await member_cursor.fetchone()
                    if not is_member or is_member[0] == 0:
                        # sent_message = await message.reply(text=LEXICON["not_a_member"])
                        sent_message = await message.reply(text="Всё хорошо, но ты не участник челленджа. Чтобы исправить это и засчитать кружок, отправь команду /start")
                    else:
                        # сделать запись в базу данных
                        await db.execute(
                            """
                            INSERT INTO events (
                                chat_title,
                                user_id,
                                username,
                                first_name,
                                last_name,
                                created_at
                            ) VALUES (?, ?, ?, ?, ?, ?)
                            """,
                            (chat_title, user_id, username, user_first_name, user_last_name, iso_date),
                        )

                        await db.commit()
                        sent_message = await message.reply(text=choice(approved))
                    # else:
                    #     sent_message = await message.reply(text=choice(not_approved))
                    await dm(sent_message, config.DELAY_VIDEO_REPLY)
        except aiosqlite.IntegrityError as e:
        # Логировать ошибку или информировать пользователя
            print(f"Integrity error: {e}")
            await message.reply(text=LEXICON["error"])


# Приветствие новых пользователей
@router.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def on_user_joined(event: ChatMemberUpdated):
    user = event.new_chat_member.user
    user_id = user.id
    user_first_name = user.first_name
    await asyncio.sleep(3)
    chat_id = event.chat.id
    sent_message = await event.bot.send_message(
        chat_id=chat_id,
        text=f"Добро пожаловать, <a href='tg://user?id={user_id}'>{user_first_name}</a>!\n"
        "Нажми команду /start, чтобы записаться в челлендж.",
        parse_mode="HTML",
    )
    await dm(sent_message, config.DELAY_GREETING)


# Ушедшеего пользователя удалить из участников
@router.chat_member(ChatMemberUpdatedFilter(IS_MEMBER >> IS_NOT_MEMBER))
async def on_user_left(event: ChatMemberUpdated):
    user = event.old_chat_member.user
    user_id = user.id
    user_first_name = user.first_name

    try:
        date = datetime.now()
        iso_date = date.strftime("%Y-%m-%d %H:%M:%S")
        async with aiosqlite.connect(DATABASE) as db:
            user_id = user.id
            async with db.execute(
                "SELECT user_id, chat_id FROM is_member WHERE user_id =? AND chat_id = ?",
                (
                    event.from_user.id,
                    event.chat.id,
                ),
            ) as cursor:
                row = await cursor.fetchone()
                await db.execute(
                    """DELETE FROM is_member WHERE user_id = ? AND chat_id = ?""",
                    (
                        int(event.from_user.id),
                        int(event.chat.id),
                    ),
                )

                await db.commit()
            await asyncio.sleep(1)
            chat_id = event.chat.id
            await event.bot.send_message(
                chat_id=chat_id,
                text=f"Пользователь, <a href='tg://user?id={user_id}'>{user_first_name}</a> больше не принимает участие в челлендже.",
                parse_mode="HTML",
            )

    except aiosqlite.IntegrityError:
        chat_id = event.chat.id
        await event.bot.send_message(chat_id=chat_id, text=LEXICON["error"])
