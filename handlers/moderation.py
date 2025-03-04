from aiogram import Bot
from aiogram.types import Message, ChatPermissions
import time

async def is_admin(bot: Bot, chat_id: int, user_id: int) -> bool:
    """Проверяет, является ли пользователь администратором или владельцем группы."""
    admins = await bot.get_chat_administrators(chat_id)
    return any(admin.user.id == user_id for admin in admins)

async def moderate_user(message: Message, bot: Bot, action: str, duration: int = None) -> None:
    """Общая функция модерации (ban, kick, mute, unmute)."""
    chat_id = message.chat.id
    user_id = message.from_user.id

    if not await is_admin(bot, chat_id, user_id):
        await message.reply("У вас нет прав для выполнения этой команды.")
        return

    if not message.reply_to_message:
        await message.reply("Эта команда должна быть использована в ответ на сообщение.")
        return

    target_user_id = message.reply_to_message.from_user.id

    if action == "ban":
        await bot.ban_chat_member(chat_id, target_user_id)
        await message.reply(f"Пользователь {target_user_id} был забанен.")
    elif action == "kick":
        await bot.ban_chat_member(chat_id, target_user_id)
        await bot.unban_chat_member(chat_id, target_user_id)
        await message.reply(f"Пользователь {target_user_id} был исключен.")
    elif action == "mute":
        until_date = int(time.time()) + duration if duration else None
        permissions = ChatPermissions(can_send_messages=False)
        await bot.restrict_chat_member(chat_id, target_user_id, permissions, until_date=until_date)
        await message.reply(f"Пользователь {target_user_id} был замучен {'на ' + str(duration) + ' секунд' if duration else 'навсегда'}.")
    elif action == "unmute":
        permissions = ChatPermissions(can_send_messages=True)
        await bot.restrict_chat_member(chat_id, target_user_id, permissions)
        await message.reply(f"Пользователь {target_user_id} был размучен.")
