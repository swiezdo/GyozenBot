import logging
from openai import OpenAI
from dialogue_styles import gyozen_style
from config import DEEPSEEK_API_KEY

# Инициализация клиента DeepSeek
client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")

async def get_response(prompt: str) -> str:
    """
    Асинхронный запрос к DeepSeek с учётом стиля Гёдзена.

    :param prompt: Вопрос от пользователя
    :return: Ответ в стиле Гёдзена
    """
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": gyozen_style},
                {"role": "user", "content": prompt}
            ],
            stream=False,
            temperature=1.3,  # Стабильность ответов
            max_tokens=1000
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"Ошибка при запросе к DeepSeek: {e}")
        return "Извините, произошла ошибка. Попробуйте ещё раз."
