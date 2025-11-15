import os
from random import choice

from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.methods import SendMessage
from aiogram.types import Message
from dotenv import load_dotenv

from comments import comments

load_dotenv()

# API_URL = "https://api.telegram.org/bot"
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(Command(commands="start"))
async def process_start_command(message: Message):
    # print(message.model_dump_json(indent=4, exclude_none=True))
    await message.reply(
        "Готово 👍\n"
        "Теперь не забывай ежедневно присылать свои кружочки.\n"
        "Иначе будешь пополнять фонд."
    )

# выписаться из челленджа /check_out
@dp.message(Command(commands="check_out"))
async def process_check_out_command(message: Message):
    # print(message.model_dump_json(indent=4, exclude_none=True))
    await message.reply("Ты успешно выписан из испытания 👋")


# Этот хэндлер будет срабатывать на команду "/help"
@dp.message(Command(commands="help"))
async def process_help_command(message: Message):
    # print(message.model_dump_json(indent=4, exclude_none=True))
    await message.reply("Что делать?\n"
    "Стоять в планке одну минуту, это как раз длительность кружочка.\n"
    "Если сегодня от тебя кружок не увидели, готовь донатик в фонд 💰")


# видео заметки
@dp.message(F.video_note)
async def process_sent_voice(message: Message):
    if message.video_note.duration > 5:
        # print(message.model_dump_json(indent=4, exclude_none=True))
        await message.reply(text=choice(comments))
    else:
        await message.reply(text="Кружок должен быть длительностью 59 секунд 🙃")



if __name__ == "__main__":
    dp.run_polling(bot)
