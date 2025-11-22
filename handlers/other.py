import asyncio
from random import choice

from aiogram import F, Router
from aiogram.filters import (IS_MEMBER, IS_NOT_MEMBER, ChatMemberUpdatedFilter,
                             Command)
from aiogram.types import ChatMemberUpdated, Message

from lexicon.lexicon import LEXICON, approved, not_approved

# инициализировать роутер уровня модуля
router = Router()


# Выписаться из челленджа /sign_out
@router.message(Command(commands="sign_out"))
async def process_check_out_command(message: Message):
    await message.reply(text=LEXICON["sign_out"])


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
