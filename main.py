import asyncio
import logging

from aiogram import Bot, Dispatcher

from config.config import Config, load_config
from handlers import other, user


async def main() -> None:
    # загрузить конфиг в переменную конфиг
    config: Config = load_config()

    # задать базовую конфигурацию логирования
    logging.basicConfig(
        level=logging.getLevelName(level=config.log.level), format=config.log.format
    )

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
