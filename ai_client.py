import logging
from openai import OpenAI
from dialogue_styles import gyozen_style
from config import AI_PROVIDER, DEEPSEEK_API_KEY, OPENAI_API_KEY, TEMPERATURE, MAX_TOKENS

# Определяем API-клиент и модель
if AI_PROVIDER == "deepseek":
    client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")
    model_name = "deepseek-chat"
elif AI_PROVIDER == "openai":
    client = OpenAI(api_key=OPENAI_API_KEY)
    model_name = "gpt-4o"
else:
    raise ValueError("Некорректное значение AI_PROVIDER в config.py. Используйте 'deepseek' или 'openai'.")

async def get_response(prompt: str) -> str:
    """
    Асинхронный запрос к AI (DeepSeek или OpenAI).
    
    :param prompt: Вопрос от пользователя
    :return: Ответ в стиле Гёдзена
    """
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": gyozen_style},
                {"role": "user", "content": prompt}
            ],
            stream=False,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"Ошибка при запросе к {AI_PROVIDER.upper()}: {e}")
        return "Извините, произошла ошибка. Попробуйте ещё раз."
