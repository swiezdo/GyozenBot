# main.py

from openai import OpenAI
from telegram import Update
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
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, respond))

    application.run_polling()

if __name__ == '__main__':
    main()
    