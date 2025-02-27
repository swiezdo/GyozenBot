# deepseek_client.py
from openai import OpenAI
from dialogue_styles import gyozen_style  # Импорт стиля из dialogue_styles.py
from config import DEEPSEEK_API_KEY
import logging

# Инициализация клиента для DeepSeek
client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")

def get_response(prompt: str) -> str:
    """
    Получает ответ от DeepSeek с учётом стиля Гёдзена.
    
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
            temperature=1.3,
            max_tokens=1000
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"Ошибка при запросе к DeepSeek: {e}")
        return "Извините, произошла ошибка. Попробуйте ещё раз."
