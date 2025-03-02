from aiogram import Bot
from aiogram.types import Message

async def is_admin(bot: Bot, chat_id: int, user_id: int) -> bool:
    """ Проверяет, является ли пользователь администратором. """
    admins = await bot.get_chat_administrators(chat_id)
    return any(admin.user.id == user_id for admin in admins)

async def ban_user(message: Message, bot: Bot) -> None:
    """ Команда /ban для бана пользователей через reply. """
    chat_id = message.chat.id
    user_id = message.from_user.id

    # Проверяем, ответил ли пользователь на сообщение
    if not message.reply_to_message:
        await message.reply("Эту команду нужно использовать в ответе на сообщение.")
        return

    # Получаем пользователя, которого хотим забанить
    user_to_ban = message.reply_to_message.from_user

    # Проверяем, является ли отправитель администратором
    if not await is_admin(bot, chat_id, user_id):
        await message.reply("У вас нет прав администратора.")
        return

    # Проверяем, является ли жертва администратором
    if await is_admin(bot, chat_id, user_to_ban.id):
        await message.reply("Нельзя забанить администратора.")
        return

    # Выполняем бан
    try:
        await bot.ban_chat_member(chat_id, user_to_ban.id)
        await message.reply(f"{user_to_ban.full_name} был(-а) забанен.")
    except Exception as e:
        await message.reply(f"Ошибка: {e}")
