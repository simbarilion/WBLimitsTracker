from telegram.ext import Application
from .config import TELEGRAM_TOKEN
from .handlers import register_handlers
from app.logging_config import setup_logger


application = Application.builder().token(TELEGRAM_TOKEN).build()
setup_logger().info("Создан экземпляр приложения")
register_handlers(application)
setup_logger().info("Зарегистрированы хэндлеры")
setup_logger(log_to_console=True).info("Бот запущен")