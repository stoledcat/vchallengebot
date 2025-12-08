from dataclasses import dataclass

from environs import Env

#TODO Выстави нормальные значения задержки
# Настройки задержек удаления сообщений
DELAY_DEFAULT = 20  # удалить ответ на команду
DELAY_ERROR_MESSAGE = 20  # ответ на ошибку
DELAY_HELP_MESSAGE = 20  # ответ на /help
DELAY_NOTIFY = 20  # уведомление
DELAY_START_MESSAGE = 20  # ответ на /start
DELAY_VIDEO_REPLY = 20  # ответ на видео
DELAY_GREETING = 20  # приветствие

VIDEO_NOTE_DURATION = 3  # длительность видео в секундах

DATABASE = "db/vchallenge.db"


@dataclass
class TgBot:
    token: str


@dataclass
class LogSettings:
    level: str
    format: str


@dataclass
class Config:
    bot: TgBot
    log: LogSettings


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        bot=TgBot(token=env("BOT_TOKEN")),
        log=LogSettings(level=env("LOG_LEVEL"), format=env("LOG_FORMAT")),
    )
