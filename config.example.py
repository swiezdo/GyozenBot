# Переименуйте в config.py

# Telegram Bot Token
TELEGRAM_TOKEN = "123"

### Выбор AI-провайдера (DeepSeek или OpenAI)
AI_PROVIDER = "deepseek"  # Можно поставить "openai" или "deepseek"

### API-ключи
DEEPSEEK_API_KEY = "123"
OPENAI_API_KEY = "123"

### Настройки генерации текста
TEMPERATURE = 1.3  # Креативность ответов
MAX_TOKENS = 1000  # Максимальное количество токенов в ответе

# Настройки DALL·E
IMAGE_MODEL = "dall-e-3"  # Можно заменить на "dall-e-3", если есть доступ
IMAGE_SIZE = "1024x1024"   # Поддерживаемые размеры: 256x256, 512x512, 1024x1024

# ID твоего Telegram-аккаунта (чтобы в ЛС бот отвечал только тебе)
OWNER_ID = 123  # Замени на свой Telegram ID

# ID группы, где бот может работать
GROUP_ID = -100123  # Замени на ID твоей группы (он всегда начинается с "-100")

# ID темы (топика) в группе, где бот может отвечать
TOPIC_ID = 123  # Замени на ID нужной темы
