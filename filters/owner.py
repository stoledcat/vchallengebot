from aiogram import Router, types
from aiogram.filters import BaseFilter

router = Router()


class OwnerFilter(BaseFilter):
    """Класс проверки, является ли пользователь администратором, владельцем"""

    async def __call__(self, message: types.Message) -> bool:
        member = await message.chat.get_member(message.from_user.id)
        # Проверяем статус члена чата
        return member.status in ("creator")
