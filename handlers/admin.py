from random import choice

import aiosqlite
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from config.config import DATABASE
from lexicon.lexicon import all_done, not_done

router = Router()


@router.message(Command(commands="stat_of_day"))
async def get_stat_of_day(message: Message):
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
            chat_id=message.chat.id, text=choice(all_done)
        )
        return

    # Сформировать список должников
    response_lines = [choice(not_done)]
    for username, user_first_name, user_last_name, last_activity in debtors:
        if username:
            response_lines.append(f"- @{username} | Последняя активность: {last_activity[:10]}")
        else:
            name = username or f"{user_first_name} {user_last_name or ''}".strip()
            response_lines.append(f"- {name} | Последняя активность: {last_activity[:10]}")

    # Отправить объединенный список всех должников
    await message.bot.send_message(
        chat_id=message.chat.id, text="\n".join(response_lines)
    )
