from aiogram import Bot
from aiogram.types import Message, ChatPermissions
from aiogram.filters import Command

async def is_admin(bot: Bot, chat_id: int, user_id: int) -> bool:
    """
    Проверяет, является ли пользователь администратором или владельцем группы.
    """
    admins = await bot.get_chat_administrators(chat_id)
    return any(admin.user.id == user_id for admin in admins)

@router.message(Command("unmute"))
async def unmute_user(message: Message, bot: Bot) -> None:
    """
    Команда /unmute для восстановления возможности отправки сообщений (reply).
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

    # Получаем пользователя, которого нужно размутить
    user_to_unmute = message.reply_to_message.from_user

    # Выполняем unmute (восстанавливаем права)
    try:
        await bot.restrict_chat_member(
            chat_id,
            user_to_unmute.id,
            permissions=ChatPermissions(can_send_messages=True)
        )
        await message.reply(f"{user_to_unmute.full_name} был(-а) размучен.")
    except Exception as e:
        await message.reply(f"Не удалось размутить {user_to_unmute.full_name}. Ошибка: {e}")
