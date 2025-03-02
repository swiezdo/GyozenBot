from aiogram import Bot
from aiogram.types import Message, ChatPermissions
from aiogram.filters import Command
import time

async def is_admin(bot: Bot, chat_id: int, user_id: int) -> bool:
    """
    Проверяет, является ли пользователь администратором или владельцем группы.
    """
    admins = await bot.get_chat_administrators(chat_id)
    return any(admin.user.id == user_id for admin in admins)

@router.message(Command("mute"))
async def mute_user(message: Message, bot: Bot) -> None:
    """
    Команда /mute для отключения возможности отправки сообщений (reply).
    """
    chat_id = message.chat.id
    user_id = message.from_user.id

    # Проверяем, является ли отправитель администратором
    if not await is_admin(bot, chat_id, user_id):
        await message.reply("У вас нет прав администратора или владельца группы.")
        return

    # Проверяем, использована ли команда в ответе на сообщение (reply)
    if not message.reply_to_message:
        await message.reply("Эту команду нужно использовать в ответе на сообщение.")
        return

    # Получаем пользователя, которого нужно замутить
    user_to_mute = message.reply_to_message.from_user

    # Проверяем, не является ли он администратором
    if await is_admin(bot, chat_id, user_to_mute.id):
        await message.reply("Нельзя замутить администратора или владельца группы.")
        return

    # Определяем длительность мута (по умолчанию 24 часа)
    try:
        duration = int(message.text.split(" ")[1]) if len(message.text.split()) > 1 else 86400
    except ValueError:
        await message.reply("Некорректный формат команды. Используйте: /mute [секунды]")
        return

    until_date = int(time.time()) + duration

    # Выполняем mute
    try:
        await bot.restrict_chat_member(
            chat_id,
            user_to_mute.id,
            permissions=ChatPermissions(can_send_messages=False),
            until_date=until_date
        )
        await message.reply(f"{user_to_mute.full_name} был(-а) замучен на {duration} секунд.")
    except Exception as e:
        await message.reply(f"Не удалось замутить {user_to_mute.full_name}. Ошибка: {e}")
