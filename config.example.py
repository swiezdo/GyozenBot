"""
config.example.py — Шаблон файла конфигурации.

Этот файл содержит примеры настроек, которые необходимо скопировать в `config.py`
и заполнить реальными значениями.

⚠️ НЕ ИЗМЕНЯЙТЕ ЭТОТ ФАЙЛ НАПРЯМУЮ! Вместо этого создайте `config.py` и вставьте туда нужные данные.
"""

# = = = ⚙️ Основные настройки = = =
AI_PROVIDER = "openai"  # "openai" или "deepseek"

# API-ключи (замените на реальные данные)
OPENAI_API_KEY = "your-openai-api-key"  # Ключ для OpenAI API
DEEPSEEK_API_KEY = "your-deepseek-api-key"  # Ключ для DeepSeek API

# Telegram Token (получите у BotFather)
TELEGRAM_TOKEN = "your-telegram-bot-token"

# = = = ⚡ Настройки AI-модели = = =
TEMPERATURE = 1.3  # Стабильность ответов (от 0 до 2, где 2 — самые креативные ответы)
MAX_TOKENS = 1000  # Максимальное количество токенов в ответе

# = = = 📌 Telegram Группа и Доступ = = =
OWNER_ID = 123456789  # ID владельца бота (узнать можно через @userinfobot)
GROUP_ID = -1001234567890  # ID группы, где работает бот (узнать можно через @username_to_id_bot)
TOPIC_ID = 12345  # ID темы, в которой бот отвечает (если нет тем, оставить None)

# = = = 🎨 Настройки генерации изображений = = =
IMAGE_MODEL = "dall-e-3"  # Или "dall-e-2", если 3-й не доступен
IMAGE_SIZE = "1024x1024"  # Размер изображения (256x256, 512x512, 1024x1024)
