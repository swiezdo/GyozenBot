from aiogram import Bot
from aiogram.types import Message, ChatPermissions
import time

async def is_admin(bot: Bot, chat_id: int, user_id: int) -> bool:
    """
    Проверяет, является ли пользователь администратором или владельцем группы.

    :param bot: Экземпляр Telegram-бота.
    :param chat_id: ID чата (группы или супергруппы).
    :param user_id: ID пользователя, которого проверяем.
    :return: True, если пользователь является админом или владельцем, иначе False.
    """
    admins = await bot.get_chat_administrators(chat_id)
    return any(admin.user.id == user_id for admin in admins)

async def moderate_user(message: Message, bot: Bot, action: str, duration: int = None) -> None:
    """
    Выполняет действия модерации (бан, кик, мут, размут) над пользователем.

    :param message: Сообщение с командой модерации.
    :param bot: Экземпляр Telegram-бота.
    :param action: Тип модерации ("ban", "kick", "mute", "unmute").
    :param duration: Время мута в секундах (если применимо).
    """
    chat_id = message.chat.id  # ID группы, где выполняется команда
    user_id = message.from_user.id  # ID отправителя команды

    # Проверяем, является ли отправитель команды админом
    if not await is_admin(bot, chat_id, user_id):
        await message.reply("⛔ У вас нет прав для выполнения этой команды.")
        return

    # Проверяем, была ли команда использована в ответ на сообщение
    if not message.reply_to_message:
        await message.reply("⚠️ Эту команду нужно использовать в ответ на сообщение.")
        return

    target_user_id = message.reply_to_message.from_user.id  # ID пользователя, к которому применяется команда

    # = = = 🛠️ Выполнение модерации = = =
    if action == "ban":
        await bot.ban_chat_member(chat_id, target_user_id)
        await message.reply(f"🚨 Пользователь {target_user_id} был забанен.")

    elif action == "kick":
        await bot.ban_chat_member(chat_id, target_user_id)  # Баним пользователя
        await bot.unban_chat_member(chat_id, target_user_id)  # Сразу разбаниваем (это кик)
        await message.reply(f"🚪 Пользователь {target_user_id} был исключен.")

    elif action == "mute":
        """
        Ограничивает возможность отправки сообщений (мут).
        Если `duration` указан, мут будет временным, иначе – постоянным.
        """
        until_date = int(time.time()) + duration if duration else None  # Дата окончания мута
        permissions = ChatPermissions(can_send_messages=False)  # Разрешения (нельзя писать)
        await bot.restrict_chat_member(chat_id, target_user_id, permissions, until_date=until_date)
        duration_text = f" на {duration} секунд" if duration else "навсегда"
        await message.reply(f"🔇 Пользователь {target_user_id} был замучен{duration_text}.")

    elif action == "unmute":
        """Снимает ограничения на отправку сообщений (размут)."""
        permissions = ChatPermissions(can_send_messages=True)  # Разрешаем снова писать
        await bot.restrict_chat_member(chat_id, target_user_id, permissions)
        await message.reply(f"🔊 Пользователь {target_user_id} был размучен.")

    else:
        await message.reply("❌ Неизвестная команда модерации.")
