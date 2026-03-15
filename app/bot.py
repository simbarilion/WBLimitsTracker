from telegram.ext import Application

from app.logging_config import setup_logger

from .config import TELEGRAM_TOKEN
from .handlers import register_handlers

logger = setup_logger(__name__)

application = Application.builder().token(TELEGRAM_TOKEN).build()
bot = application.bot
logger.info("Создан экземпляр приложения")
register_handlers(application)
logger.info("Зарегистрированы хэндлеры")
logger.info("Бот инициализирован")
