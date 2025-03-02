import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from config import TELEGRAM_TOKEN
from handlers.ban import ban_user
from handlers.kick import kick_user
from handlers.mute import mute_user
from handlers.unmute import unmute_user
from message_handlers import start, respond  # ✅ Импортируем обработчики сообщений

# Настраиваем логирование
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# ✅ Регистрируем команды
dp.message.register(start, Command("start"))  # Команда /start
dp.message.register(ban_user, Command("ban"))
dp.message.register(kick_user, Command("kick"))
dp.message.register(mute_user, Command("mute"))
dp.message.register(unmute_user, Command("unmute"))

# ✅ Регистрируем обработчик обычных сообщений (ответы ИИ)
dp.message.register(respond)

async def main():
    """Основная асинхронная функция запуска бота."""
    logging.info("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
