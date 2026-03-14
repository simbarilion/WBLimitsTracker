import sqlite3
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from .services import check_limits
from .config import DB, TELEGRAM_TOKEN
import telegram
from app.logging_config import setup_logger

bot = telegram.Bot(token=TELEGRAM_TOKEN)

last_run_time = None

def scheduled_check():
    global last_run_time
    last_run_time = datetime.now()

    conn = sqlite3.connect(DB)
    setup_logger().info(f"Соединение с базой данных {DB} открыто")
    cur = conn.cursor()
    cur.execute('SELECT chat_id, api_key, warehouses, paid FROM users')
    rows = cur.fetchall()
    setup_logger().info(f"Получены данные из базы данных {DB}")
    conn.close()
    setup_logger().info(f"Соединение с базой данных {DB} закрыто")
    for row in rows:
        chat_id, api_key, whs, paid = row
        if whs and paid:
            msg = check_limits(api_key, whs)
            if 'Available' in msg:
                try:
                    bot.send_message(chat_id=chat_id, text=msg)
                except Exception as e:
                    setup_logger().error(f"Ошибка отправки сообщения {e}")

def start_scheduler():
    scheduler = BackgroundScheduler()
    setup_logger().info(f"Создан объект планировщика задач BackgroundScheduler")
    scheduler.add_job(scheduled_check, 'interval', hours=1)
    scheduler.start()
    setup_logger().info(f"Планировщик задач scheduler запущен")
