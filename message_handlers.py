import time
import random
import re
from aiogram.types import Message
from ai_client import get_response
from waiting_phrases import WAITING_PHRASES
from image_generator import generate_image

# = = = Конфигурация = = =
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
    Обработка текстовых сообщений с использованием ИИ.
    """
    message_time = message.date.timestamp()
    user_message = message.text.lower().strip()
    chat_type = message.chat.type

    # Проверка времени и релевантности сообщения
    if not is_recent_message(message_time) or not is_relevant_message(user_message, chat_type):
        return

    # = = = Проверка запроса на генерацию изображения = = =
    if re.search(r"г[ёе]дзен.*создай изображение", user_message):
        prompt = user_message.split("создай изображение", 1)[-1].strip()

        if not prompt:
            await message.reply("Опиши, что ты хочешь увидеть!")
            return

        await message.reply("Генерирую изображение... 🎨🔄")

        # Генерация изображения
        image_url = await generate_image(prompt)
        if image_url:
            await message.reply_photo(image_url, caption="Вот твое изображение! 🎭")
        else:
            await message.reply("Произошла ошибка при создании изображения. 😢")
        return  # Завершаем обработку, если запрос был связан с изображением

    # = = = Обычная генерация текста = = =
    waiting_phrase = random.choice(WAITING_PHRASES)
    waiting_message = await message.answer(waiting_phrase)

    # Получаем и отправляем ответ
    response = await get_response(user_message)
    await waiting_message.edit_text(response)
