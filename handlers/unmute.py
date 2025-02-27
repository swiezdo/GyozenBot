# Команда /unmute для восстановления возможности отправки сообщений (reply)
from telegram import Update
from telegram.ext import ContextTypes
import time

async def unmute_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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
    user_to_unmute = update.message.reply_to_message.from_user
    
    # Выполняем unmute (восстанавливаем все права)
    try:
        await context.bot.restrict_chat_member(
            chat_id, 
            user_to_unmute.id,
            permissions={'can_send_messages': True}
        )
        await update.message.reply_text(f"{user_to_unmute.full_name} был размучен.")
    except Exception as e:
        await update.message.reply_text(f"Не удалось размутить {user_to_unmute.full_name}. Ошибка: {e}")
