import logging
from openai import OpenAI
from config import AI_PROVIDER, DEEPSEEK_API_KEY, OPENAI_API_KEY, TEMPERATURE, MAX_TOKENS, FINE_TUNED_MODEL
from dialogue_styles import gyozen_style  # Подключаем стиль Гёдзена

# Подключаем API-клиента в зависимости от выбранного провайдера
if AI_PROVIDER == "deepseek":
    client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")
    model_name = "deepseek-chat"
elif AI_PROVIDER == "openai":
    client = OpenAI(api_key=OPENAI_API_KEY)
    model_name = FINE_TUNED_MODEL if FINE_TUNED_MODEL else "gpt-4o"
else:
    raise ValueError("Некорректное значение AI_PROVIDER в config.py. Используйте 'deepseek' или 'openai'.")

async def get_response(prompt: str) -> str:
    """
    Отправляет запрос к AI (Fine-Tuned модель, стандартный OpenAI или DeepSeek) и получает ответ.

    :param prompt: Вопрос от пользователя.
    :return: Сгенерированный AI-ответ.
    """
    try:
        # Определяем, какой формат сообщений использовать
        if AI_PROVIDER == "openai" and FINE_TUNED_MODEL:
            # Если выбран OpenAI и есть Fine-Tuned модель, используем только user prompt
            messages = [{"role": "user", "content": prompt}]
        else:
            # Если используется обычный GPT-4o или DeepSeek, добавляем стиль Гёдзена
            messages = [
                {"role": "system", "content": gyozen_style},
                {"role": "user", "content": prompt}
            ]

        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            stream=False,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"Ошибка при запросе к {AI_PROVIDER.upper()}: {e}")
        return "Извините, произошла ошибка. Попробуйте ещё раз."
