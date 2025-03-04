import logging
from openai import OpenAI
from config import AI_PROVIDER, OPENAI_API_KEY, IMAGE_MODEL, IMAGE_SIZE

# Подключаем OpenAI API
client = OpenAI(api_key=OPENAI_API_KEY)

async def generate_image(prompt: str) -> str:
    """
    Генерация изображения с помощью OpenAI DALL·E.

    :param prompt: Описание изображения.
    :return: URL созданного изображения.
    """
    try:
        response = client.images.generate(
            model=IMAGE_MODEL,
            prompt=prompt,
            size=IMAGE_SIZE,
            n=1  # Количество изображений (можно больше)
        )
        return response.data[0].url
    except Exception as e:
        logging.error(f"Ошибка генерации изображения: {e}")
        return None
