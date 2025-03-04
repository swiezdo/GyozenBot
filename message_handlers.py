import time
import random
import re
from aiogram.types import Message
from ai_client import get_response
from waiting_phrases import WAITING_PHRASES
from image_generator import generate_image
from config import OWNER_ID, GROUP_ID, TOPIC_ID  # Импортируем ограничения

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

def is_relevant_message(message: Message) -> bool:
    """
    Проверяет, можно ли боту отвечать на сообщение.
    - В ЛС отвечает только владельцу.
    - В группе отвечает только в указанной группе и теме.
    """
    chat_type = message.chat.type

    # 1️⃣ **Личные сообщения** (бот отвечает только OWNER_ID)
    if chat_type == "private":
        return message.from_user.id == OWNER_ID

    # 2️⃣ **Группы / Супергруппы**
    if chat_type in ["group", "supergroup"]:
        if message.chat.id != GROUP_ID:  # Если это не наша группа — игнорируем
            return False

        # **Если в группе включены темы, сообщение должно быть в нужной теме**
        if message.is_topic_message:  # Проверяем, что это сообщение в теме
            if message.message_thread_id != TOPIC_ID:  # Не наша тема — игнорируем
                return False
        else:
            # Если в группе есть темы, а сообщение НЕ в теме — игнорируем
            return False

        return True  # Все проверки пройдены, можно отвечать

    return False  # Остальные случаи игнорируем


async def respond(message: Message) -> None:
    """
    Обработка текстовых сообщений с использованием ИИ.
    """
    message_time = message.date.timestamp()
    user_message = message.text.lower().strip() if message.text else ""

    # Проверка, можно ли боту отвечать
    if not user_message or not is_recent_message(message_time) or not is_relevant_message(message):
        return  # Игнорируем пустые сообщения и неподходящие чаты

    # Проверяем, есть ли "Гёдзен" в сообщении (с разными вариантами написания)
    if not re.search(r"г[ёе]д[зс][еэ]н", user_message, re.IGNORECASE):
        return  # Игнорируем сообщения без упоминания "Гёдзен"

    # = = = Проверка запроса на генерацию изображения = = =
    match = re.search(r"г[ёе]д[зс][еэ]н.*создай изображение", user_message, re.IGNORECASE)
    if match:
        prompt = user_message[match.end():].strip()  # Берем текст после "создай изображение"

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
