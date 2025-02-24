# main.py

import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from config import TELEGRAM_TOKEN, OPENAI_API_KEY
from dialogue_styles import gyozen_style  # Импорт стиля из dialogue_styles.py

# Настройка OpenAI
openai.api_key = OPENAI_API_KEY

# Функция для получения ответа от ChatGPT с учётом стиля Гёдзена
def get_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": gyozen_style},  # Добавляем стиль Гёдзена
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000,
        temperature=0.8,
    )
    # Извлекаем ответ по рабочему синтаксису OpenAI
    return response['choices'][0]['message']['content'].strip()

# Обработка команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Привет! Я ChatGPT-бот в стиле Гёдзена. Задай мне любой вопрос.")

# Обработка сообщений (только ChatGPT)
async def respond(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
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
