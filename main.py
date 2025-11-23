import asyncio
import logging

import aiosqlite
from aiogram import Bot, Dispatcher

from config.config import Config, load_config
from handlers import other, user
from lexicon.lexicon import LEXICON


async def main() -> None:
    # загрузить конфиг в переменную конфиг
    config: Config = load_config()

    # Задать базовую конфигурацию логирования
    logging.basicConfig(
        level=logging.getLevelName(level=config.log.level), format=config.log.format
    )

    # Создать базу данных
    async with aiosqlite.connect(LEXICON["database"]) as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                joined_at TEXT,
                left_at TEXT,
                chat_id INTEGER,
                is_member INTEGER
            )
            """
        )
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS events (
                event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER,
                user_id INTEGER,
                username TEXT,
                user_first_name TEXT,
                user_last_name TEXT,
                is_complete INTEGER,
                created_at TEXT,
                penalty INTEGER,
                FOREIGN KEY(user_id) REFERENCES users(user_id)
            )
            """
        )
        await db.commit()

    # инициализировать бота и дспетчера
    bot = Bot(token=config.bot.token)
    dp = Dispatcher()

    dp.include_router(user.router)
    dp.include_router(other.router)

    # пропустить накопившиеся апдейты
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
