from aiogram.exceptions import TelegramBadRequest
import asyncio
import handlers.delay as delay


# TODO изменить задержку уаления сообщений по умолчанию
# автоматическое удаление  сообщений
async def delete_message_delayed(message, delay_seconds: int = delay.DELAY_DEFAULT):
    await asyncio.sleep(delay_seconds)
    try:
        await message.delete()
    except TelegramBadRequest as e:
        # Игнорировать ошибки удаления, например, если сообщение уже удалено или нельзя удалить
        if (
            "message to delete not found" in str(e).lower()
            or "message can't be deleted" in str(e).lower()
        ):
            pass
        else:
            raise
