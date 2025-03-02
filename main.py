import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from config import TELEGRAM_TOKEN
from handlers.ban import ban_user
from handlers.kick import kick_user
from handlers.mute import mute_user
from handlers.unmute import unmute_user

# Настраиваем логирование
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# ✅ Регистрируем команды вручную (без `include_router`)
dp.message.register(ban_user, Command("ban"))
dp.message.register(kick_user, Command("kick"))
dp.message.register(mute_user, Command("mute"))
dp.message.register(unmute_user, Command("unmute"))

# ✅ Тестовая команда (проверка)
@dp.message(Command("test"))
async def test_command(message: Message):
    logging.debug("✅ Вызван обработчик команды /test!")
    await message.answer("Бот работает! 🚀")

async def main():
    """Основная асинхронная функция запуска бота."""
    logging.info("Бот запущен...")
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    asyncio.run(main())
