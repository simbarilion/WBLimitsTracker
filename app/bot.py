import os

from telegram.ext import Application
from .config import TELEGRAM_TOKEN
from .handlers import register_handlers
from app.logging_config import setup_logger


logger = setup_logger(__name__)

application = Application.builder().token(TELEGRAM_TOKEN).build()
bot = application.bot
logger.info("Создан экземпляр приложения")
register_handlers(application)
logger.info("Зарегистрированы хэндлеры")
logger.info("Бот инициализирован")
