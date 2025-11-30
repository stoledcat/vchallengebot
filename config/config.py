from dataclasses import dataclass

from environs import Env

#TODO Выстави нормальные значения задержки
DELAY_DEFAULT = 60
DELAY_ERROR_MESSAGE = 60
DELAY_HELP_MESSAGE = 120
DELAY_NOTIFY = 120
DELAY_START_MESSAGE = 120
DELAY_VIDEO_REPLY = 120
DELAY_GREETING = 120
VIDEO_NOTE_DURATION = 59

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
