import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from config import TELEGRAM_TOKEN
from handlers.moderation import moderate_user
from message_handlers import start, respond

# Настраиваем логирование
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(message)s",
)

# Создаем бота и диспетчер
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# Регистрируем обработчики команд
dp.message.register(start, Command("start"))
dp.message.register(respond)

# Регистрируем команды модерации
async def handle_ban(message):
    await moderate_user(message, bot, "ban")

async def handle_kick(message):
    await moderate_user(message, bot, "kick")

async def handle_mute(message):
    await moderate_user(message, bot, "mute", duration=3600)

async def handle_unmute(message):
    await moderate_user(message, bot, "unmute")

dp.message.register(handle_ban, Command("ban"))
dp.message.register(handle_kick, Command("kick"))
dp.message.register(handle_mute, Command("mute"))
dp.message.register(handle_unmute, Command("unmute"))

async def main():
    """Запуск бота."""
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
