# main.py

from openai import OpenAI
from telegram import Update, ChatMemberOwner, ChatMemberAdministrator
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from dialogue_styles import gyozen_style  # Импорт стиля из dialogue_styles.py
from config import TELEGRAM_TOKEN, DEEPSEEK_API_KEY  # Импорт ключей из config.py
import time  # Для проверки времени сообщений
import re  # Для проверки слов в сообщениях

# Инициализация клиента для DeepSeek
client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")

# Порог времени в секундах (сообщения старше этого времени игнорируются)
TIME_THRESHOLD = 60  # 60 секунд

# Регулярное выражение для проверки слов в любом регистре
PATTERN = re.compile(r"г[ёе]д[зс][еэ]н", re.IGNORECASE)

# Функция для получения ответа от DeepSeek с учётом стиля Гёдзена
def get_response(prompt):
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": gyozen_style},
            {"role": "user", "content": prompt}
        ],
        stream=False,
        temperature=1.3,
        max_tokens=1000
    )
    return response.choices[0].message.content.strip()

# Обработка команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Привет! Я бот в стиле Гёдзена, использующий DeepSeek. Задай мне любой вопрос.")

# Команда /ban для бана пользователей через ответ на сообщение (reply)
async def ban_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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
    user_to_ban = update.message.reply_to_message.from_user
    
    # Проверяем, не является ли пользователь администратором или владельцем группы
    for admin in admins:
        if admin.user.id == user_to_ban.id:
            await update.message.reply_text("Нельзя забанить администратора или владельца группы.")
            return
    
    # Выполняем бан
    try:
        await context.bot.ban_chat_member(chat_id, user_to_ban.id)
        await update.message.reply_text(f"{user_to_ban.full_name} был забанен.")
    except Exception as e:
        await update.message.reply_text(f"Не удалось забанить {user_to_ban.full_name}. Ошибка: {e}")

# Обработка сообщений (только DeepSeek)
async def respond(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Проверка времени сообщения
    message_time = update.message.date.timestamp()  # Время сообщения в timestamp
    current_time = time.time()  # Текущее время в timestamp

    # Если сообщение старше TIME_THRESHOLD секунд, игнорируем его
    if current_time - message_time > TIME_THRESHOLD:
        return

    user_message = update.message.text
    
    # Проверяем тип чата
    if update.message.chat.type in ["group", "supergroup"]:
        # В группах отвечаем только если есть слово "Гёдзен", "Гедзен", "Гёдзэн" или "Гедзэн" в любом регистре
        if not PATTERN.search(user_message):
            return

    # В личных сообщениях отвечаем на любое сообщение
    response = get_response(user_message)
    await update.message.reply_text(response)

# Основная функция
def main():
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("ban", ban_user))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, respond))

    application.run_polling()

if __name__ == '__main__':
    main()
