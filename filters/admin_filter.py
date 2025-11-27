from aiogram import Router, types
from aiogram.filters import BaseFilter

router = Router()


class AdminFilter(BaseFilter):
    """Класс проверки, является ли пользователь администратором, владельцем"""

    async def __call__(self, message: types.Message) -> bool:
        member = await message.chat.get_member(message.from_user.id)
        # Проверяем статус члена чата
        return member.status in ("administrator", "creator")


# @router.message(AdminFilter(), Command("admin"))
# async def admin_only_handler(message: types.Message):
#     await message.reply("Вы администратор!")
