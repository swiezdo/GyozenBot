# main.py
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from config import TELEGRAM_TOKEN
from message_handlers import start, respond
from handlers.ban import ban_user
from handlers.kick import kick_user
from handlers.mute import mute_user
from handlers.unmute import unmute_user

def main() -> None:
    """
    Основная функция запуска бота.
    """
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("ban", ban_user))
    application.add_handler(CommandHandler("kick", kick_user))
    application.add_handler(CommandHandler("mute", mute_user))
    application.add_handler(CommandHandler("unmute", unmute_user))

    # Обработчик сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, respond))

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()
