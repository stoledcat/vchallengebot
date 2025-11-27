import aiosqlite
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
# from filters.admin_filter import AdminFilter

from config.config import DATABASE

router = Router()


# @router.message(AdminFilter(), Command(commands="stat_of_day"))
@router.message(Command(commands="stat_of_day"))
async def get_stat_of_day(message: Message):
    chat_id = message.chat.id  # текущий чат
    async with aiosqlite.connect(DATABASE) as db:
        query = """
        SELECT u.user_id, u.username, u.first_name, u.last_name
        FROM users u
        JOIN events e ON u.user_id = e.user_id AND e.chat_id = ?
        WHERE u.is_member = 1
        AND u.user_id NOT IN (
            SELECT user_id
            FROM events
            WHERE chat_id = ?
            AND DATE(created_at) = DATE('now', 'localtime')
        )
        """
        await message.delete()

        async with aiosqlite.connect(DATABASE) as db:
            async with db.execute(query, (chat_id, chat_id)) as cursor:
                rows = await cursor.fetchall()

        # BUG разобраться с списком пользователей
        if not rows:
            await message.bot.send_message(
                chat_id=message.chat.id,
                text="Сегодня все активны, нет пользователей без видео заметок.",
            )

            return

        response_lines = ["Пользователи без видео заметок сегодня:"]

        for user_id, username, first_name, last_name in rows:
            name = username or f"{first_name or ''} {last_name or ''}".strip()
            response_lines.append(f"- {name} (id: {user_id})")

        await message.reply("\n".join(response_lines))
