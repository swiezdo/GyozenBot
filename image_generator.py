import logging
from openai import OpenAI
from config import AI_PROVIDER, OPENAI_API_KEY, IMAGE_MODEL, IMAGE_SIZE

# Подключаем OpenAI API для генерации изображений
client = OpenAI(api_key=OPENAI_API_KEY)

async def generate_image(prompt: str) -> str:
    """
    Генерирует изображение с помощью OpenAI DALL·E.

    :param prompt: Описание изображения.
    :return: URL созданного изображения (или None, если ошибка).
    """
    try:
        response = client.images.generate(
            model=IMAGE_MODEL,
            prompt=prompt,
            size=IMAGE_SIZE,
            n=1  # Можно изменить, чтобы генерировать больше изображений
        )
        return response.data[0].url
    except Exception as e:
        logging.error(f"Ошибка при генерации изображения: {e}")
        return None
