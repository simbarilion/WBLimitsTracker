import telegram
from telegram.ext import Application
from .config import TELEGRAM_TOKEN
from .handlers import register_handlers
from app.logging_config import setup_logger


logger = setup_logger(__name__)

application = Application.builder().token(TELEGRAM_TOKEN).build()
logger.info("Создан экземпляр приложения")
register_handlers(application)
logger.info("Зарегистрированы хэндлеры")
setup_logger(log_to_console=True).info("Бот запущен")

bot = telegram.Bot(token=TELEGRAM_TOKEN)