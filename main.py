import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from config import TELEGRAM_TOKEN
from handlers.moderation import moderate_user
from message_handlers import start, respond

# Настраиваем логирование (будет писать ошибки и важные события)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(message)s",
)

# Создаем бота и диспетчер для обработки сообщений
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# Регистрируем обработчики команд
dp.message.register(start, Command("start"))  # Команда /start
dp.message.register(respond)  # Все остальные сообщения

# Функции для команд модерации
async def handle_ban(message):
    """Бан пользователя (запрещает вход в чат)."""
    await moderate_user(message, bot, "ban")

async def handle_kick(message):
    """Кик пользователя (исключает, но позволяет вернуться)."""
    await moderate_user(message, bot, "kick")

async def handle_mute(message):
    """Мут (запрещает отправку сообщений на 1 час)."""
    await moderate_user(message, bot, "mute", duration=3600)

async def handle_unmute(message):
    """Размут (возвращает право писать сообщения)."""
    await moderate_user(message, bot, "unmute")

# Регистрируем команды модерации
dp.message.register(handle_ban, Command("ban"))
dp.message.register(handle_kick, Command("kick"))
dp.message.register(handle_mute, Command("mute"))
dp.message.register(handle_unmute, Command("unmute"))

async def main():
    """Запускаем бота."""
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
