# Команда /mute для отключения возможности отправки сообщений (reply)
from telegram import Update
from telegram.ext import ContextTypes
import time

async def mute_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    # Получаем список администраторов и владельца группы
    admins = await context.bot.get_chat_administrators(chat_id)
    is_admin = False
    
    # Проверяем, является ли пользователь администратором или владельцем группы
    for admin in admins:
        if admin.user.id == user_id:
            is_admin = True
            break

    # Если пользователь не администратор и не владелец группы — отказ
    if not is_admin:
        await update.message.reply_text("У вас нет прав администратора или владельца группы.")
        return
    
    # Проверяем, используется ли команда в ответе на сообщение (reply)
    if not update.message.reply_to_message:
        await update.message.reply_text("Эту команду нужно использовать в ответе на сообщение.")
        return

    # Получаем пользователя, на сообщение которого был сделан ответ
    user_to_mute = update.message.reply_to_message.from_user
    
    # Проверяем, не является ли пользователь администратором или владельцем группы
    for admin in admins:
        if admin.user.id == user_to_mute.id:
            await update.message.reply_text("Нельзя замутить администратора или владельца группы.")
            return
    
    # Проверяем, указано ли время mute
    duration = int(context.args[0]) if context.args else 86400  # По умолчанию 24 часа
    until_date = int(time.time()) + duration
    
    # Выполняем mute
    try:
        await context.bot.restrict_chat_member(
            chat_id, 
            user_to_mute.id,
            permissions={'can_send_messages': False},
            until_date=until_date
        )
        await update.message.reply_text(f"{user_to_mute.full_name} был замучен на {duration} секунд.")
    except Exception as e:
        await update.message.reply_text(f"Не удалось замутить {user_to_mute.full_name}. Ошибка: {e}")
