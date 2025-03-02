import time
import random
import re
from aiogram.types import Message
from deepseek_client import get_response
from waiting_phrases import WAITING_PHRASES

# === Конфигурация ===
TIME_THRESHOLD = 60  # 60 секунд
PATTERN = re.compile(r"г[ёе]д[зс][еэ]н", re.IGNORECASE)

async def start(message: Message) -> None:
    """
    Обработка команды /start.
    """
    await message.answer("Привет! Я бот в стиле Гёдзена, использующий DeepSeek. Задай мне любой вопрос.")

def is_recent_message(message_time: float) -> bool:
    """
    Проверка, является ли сообщение недавним.
    """
    return time.time() - message_time <= TIME_THRESHOLD

def is_relevant_message(message_text: str, chat_type: str) -> bool:
    """
    Проверка, следует ли отвечать на сообщение.
    В группах отвечает только если в сообщении есть упоминание Гёдзена.
    """
    if chat_type in ["group", "supergroup"]:
        return bool(PATTERN.search(message_text))
    return True

async def respond(message: Message) -> None:
    """
    Обработка текстовых сообщений с использованием DeepSeek.
    """
    message_time = message.date.timestamp()
    user_message = message.text
    chat_type = message.chat.type

    # Проверка времени и релевантности сообщения
    if not is_recent_message(message_time) or not is_relevant_message(user_message, chat_type):
        return

    # Выбираем случайную фразу ожидания
    waiting_phrase = random.choice(WAITING_PHRASES)
    waiting_message = await message.answer(waiting_phrase)

    # Получаем и отправляем ответ
    response = await get_response(user_message)  # Делаем вызов асинхронным!
    await waiting_message.edit_text(response)
