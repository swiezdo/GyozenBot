from aiogram import Bot
from aiogram.types import Message

async def is_admin(bot: Bot, chat_id: int, user_id: int) -> bool:
    """
    Проверяет, является ли пользователь администратором или владельцем группы.
    """
    admins = await bot.get_chat_administrators(chat_id)
    return any(admin.user.id == user_id for admin in admins)

async def kick_user(message: Message, bot: Bot) -> None:
    """
    Команда /kick для исключения пользователя без бана.
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

    # Получаем пользователя, которого нужно исключить
    user_to_kick = message.reply_to_message.from_user

    # Проверяем, не является ли он администратором
    if await is_admin(bot, chat_id, user_to_kick.id):
        await message.reply("Нельзя исключить администратора или владельца группы.")
        return

    # Выполняем исключение (без бана)
    try:
        await bot.ban_chat_member(chat_id, user_to_kick.id, revoke_messages=False)  # Исключаем (без удаления сообщений)
        await bot.unban_chat_member(chat_id, user_to_kick.id)  # Разбан (чтобы мог сразу вернуться)
        await message.reply(f"{user_to_kick.full_name} был(-а) исключён, но может вернуться.")
    except Exception as e:
        await message.reply(f"Не удалось исключить {user_to_kick.full_name}. Ошибка: {e}")
