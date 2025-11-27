import asyncio
import logging

import aiosqlite
from aiogram import Bot, Dispatcher

from config.config import DATABASE, Config, load_config
from db import db_scheme
from handlers import admin, other, user


async def main() -> None:
    # Загрузить конфиг в переменную конфиг
    config: Config = load_config()

    # Задать базовую конфигурацию логирования
    logging.basicConfig(
        level=logging.getLevelName(level=config.log.level), format=config.log.format
    )

    # Создать базу данных
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute(db_scheme.chats)
        await db.execute(db_scheme.users)
        await db.execute(db_scheme.events)
        await db.commit()

    # инициализировать бота и дспетчера
    bot = Bot(token=config.bot.token)
    dp = Dispatcher()

    dp.include_router(admin.router)
    dp.include_router(other.router)
    dp.include_router(user.router)

    # пропустить накопившиеся апдейты
    # await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
