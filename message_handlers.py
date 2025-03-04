import time
import random
import re
from aiogram.types import Message
from ai_client import get_response
from waiting_phrases import WAITING_PHRASES
from image_generator import generate_image
from config import OWNER_ID, GROUP_ID, TOPIC_ID  # Импортируем ограничения

# Конфигурация
TIME_THRESHOLD = 60  # Максимальное время (в секундах) для ответа
PATTERN = re.compile(r"г[ёе]д[зс][еэ]н", re.IGNORECASE)  # Поиск слова "Гёдзен"

async def start(message: Message) -> None:
    """Ответ на команду /start."""
    await message.answer("Привет! Я бот в стиле Гёдзена. Задай мне вопрос.")

def is_recent_message(message_time: float) -> bool:
    """Проверяет, не слишком ли старое сообщение."""
    return time.time() - message_time <= TIME_THRESHOLD

def is_relevant_message(message: Message) -> bool:
    """
    Проверяет, можно ли боту отвечать на это сообщение.
    - В ЛС отвечает только владельцу.
    - В группе отвечает только в указанной группе и теме.
    """
    chat_type = message.chat.type

    # Личные сообщения (бот отвечает только владельцу)
    if chat_type == "private":
        return message.from_user.id == OWNER_ID

    # Проверяем группу и тему
    if chat_type in ["group", "supergroup"]:
        if message.chat.id != GROUP_ID:  # Бот работает только в одной группе
            return False

        # Если в группе есть темы, сообщение должно быть в указанной теме
        if message.is_topic_message and message.message_thread_id != TOPIC_ID:
            return False

        return True

    return False  # Остальные случаи игнорируем

async def respond(message: Message) -> None:
    """Обработка сообщений с AI-ответами."""
    message_time = message.date.timestamp()
    user_message = message.text.lower().strip() if message.text else ""

    # Проверка, можно ли отвечать
    if not user_message or not is_recent_message(message_time) or not is_relevant_message(message):
        return

    # Бот отвечает только если в сообщении есть "Гёдзен"
    if not re.search(PATTERN, user_message):
        return

    # Проверка генерации изображений
    match = re.search(r"г[ёе]д[зс][еэ]н.*создай изображение", user_message, re.IGNORECASE)
    if match:
        prompt = user_message[match.end():].strip()
        if not prompt:
            await message.reply("Опиши, что ты хочешь увидеть!")
            return

        await message.reply("Генерирую изображение... 🎨🔄")
        image_url = await generate_image(prompt)
        if image_url:
            await message.reply_photo(image_url, caption="Вот твое изображение! 🎭")
        else:
            await message.reply("Ошибка при создании изображения. 😢")
        return

    # Обычный AI-ответ
    waiting_phrase = random.choice(WAITING_PHRASES)
    waiting_message = await message.answer(waiting_phrase)
    response = await get_response(user_message)
    await waiting_message.edit_text(response)
