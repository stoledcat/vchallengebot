import asyncio
from random import choice
import aiosqlite
from datetime import datetime

from aiogram import F, Router
from aiogram.filters import IS_MEMBER, IS_NOT_MEMBER, ChatMemberUpdatedFilter, Command
from aiogram.types import ChatMemberUpdated, Message

from lexicon.lexicon import LEXICON, approved, not_approved

# инициализировать роутер уровня модуля
router = Router()


# Выписаться из челленджа /sign_out
@router.message(Command(commands="sign_out"))
async def process_check_out_command(message: Message):
    try:
        date = datetime.now()
        iso_date = date.strftime("%Y-%m-%d %H:%M:%S")
        async with aiosqlite.connect("app/vplanke.db") as db:
            user = message.from_user
            user_id = user.id
            async with db.execute(
                "SELECT is_member FROM users WHERE user_id = ?", (user_id,)
            ) as cursor:
                row = await cursor.fetchone()
            if not row:
                await message.reply(text=LEXICON["not_in_base"])
            elif row[0] == 0:
                await message.reply(text=LEXICON["already_signed_out"])
            else:
                await db.execute(
                    """
                    UPDATE users
                    SET left_at = ?, is_member = ?
                    WHERE user_id = ?
                    """,
                    (iso_date, 0, user.id),
                )

                await db.commit()
                await message.reply(text=LEXICON["sign_out"])
    except aiosqlite.IntegrityError as e:
        # Логировать ошибку или информировать пользователя
        print(f"Integrity error: {e}")
        await message.reply(text=LEXICON["error"])


# Проверка видео аметок (кружочков)
@router.message(F.video_note)
async def process_sent_voice(message: Message):
    if message.video_note.duration > 59:
        # print(message.model_dump_json(indent=4, exclude_none=True))
        await message.reply(text=choice(approved))
    else:
        await message.reply(text=choice(not_approved))


# Приветствие новых пользователей
@router.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def on_user_joined(event: ChatMemberUpdated):
    user = event.new_chat_member.user
    user_id = user.id
    user_first_name = user.first_name
    await asyncio.sleep(5)
    chat_id = event.chat.id
    await event.bot.send_message(
        chat_id=chat_id,
        text=f"Добро пожаловать, <a href='tg://user?id={user_id}'>{user_first_name}</a>!\n"
        "Нажми команду /start, чтобы записаться в челлендж.",
        parse_mode="HTML",
    )


# Вышедшему пользователю установить is_member = 0
@router.chat_member(ChatMemberUpdatedFilter(IS_MEMBER >> IS_NOT_MEMBER))
async def on_user_left(event: ChatMemberUpdated):
    user = event.old_chat_member.user
    user_id = user.id
    user_first_name = user.first_name

    try:
        date = datetime.now()
        iso_date = date.strftime("%Y-%m-%d %H:%M:%S")
        async with aiosqlite.connect("app/vplanke.db") as db:
            user_id = user.id
            async with db.execute(
                "SELECT is_member FROM users WHERE user_id = ?", (user_id,)
            ) as cursor:
                row = await cursor.fetchone()
                await db.execute(
                    """
                    UPDATE users
                    SET left_at = ?, is_member = ?
                    WHERE user_id = ?
                    """,
                    (iso_date, 0, user.id),
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
