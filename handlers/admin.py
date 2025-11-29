from random import choice

import aiosqlite
from aiogram import Bot, Router, types
from aiogram.filters import Command
from aiogram.types import Message

from config.config import DATABASE
from lexicon.lexicon import all_done, not_done

router = Router()


@router.message(Command(commands="stat_of_day"))
async def get_stat_of_day(message: Message):
    user_id = message.from_user.id
    # Удалить сообщение
    await message.delete()
    response_lines = []

    async with aiosqlite.connect(DATABASE) as db:
        query = """
        SELECT username, user_first_name, user_last_name, last_activity FROM users
        WHERE (last_activity IS NULL OR date(last_activity) < date('now')) AND is_member == 1
        """

        async with db.execute(query) as cursor:
            debtors = await cursor.fetchall()

    if not debtors:
        await message.bot.send_message(
            user_id, text=choice(all_done)
        )
        return

    # Сформировать список должников
    response_lines = [choice(not_done)]
    for username, user_first_name, user_last_name, _ in debtors:
        if username:
            response_lines.append(f"- @{username}")
        else:
            name = username or f"{user_first_name} {user_last_name or ''}".strip()
            response_lines.append(f"- {name}")

    # Отправить объединенный список всех должников
    await message.bot.send_message(
        user_id, text="\n".join(response_lines)
    )
