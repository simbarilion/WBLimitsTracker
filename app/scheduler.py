from datetime import datetime
from typing import Optional

from apscheduler.schedulers.background import BackgroundScheduler

from .services import check_limits
from .config import TELEGRAM_TOKEN
import telegram
from app.logging_config import setup_logger
from .user_repository import get_users

logger = setup_logger(__name__)

bot = telegram.Bot(token=TELEGRAM_TOKEN)

last_run_time: Optional[datetime] = None

def scheduled_check() -> None:
    """Периодически проверяет лимиты складов для платных пользователей и отправляет уведомления"""
    global last_run_time
    last_run_time = datetime.now()

    rows = get_users()
    for row in rows:
        chat_id, api_key, whs, paid = row
        if whs and paid:
            msg = check_limits(api_key, whs)
            if "Available" in msg:
                try:
                    bot.send_message(chat_id=chat_id, text=msg)
                except Exception as e:
                    logger.error(f"Ошибка отправки сообщения {e}")


def start_scheduler() -> None:
    """Запускает планировщик задач для регулярной проверки лимитов"""
    scheduler = BackgroundScheduler()
    logger.info(f"Создан объект планировщика задач BackgroundScheduler")
    scheduler.add_job(scheduled_check, "interval", hours=1)
    scheduler.start()
    logger.info(f"Планировщик задач scheduler запущен")
