import sqlite3
import os
from .config import DB
from app.logging_config import setup_logger

def init_db():
    dir_path = os.path.dirname(DB)
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)
    conn = sqlite3.connect(DB)
    setup_logger().info(f"Соединение с базой данных {DB} открыто")
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS users
                 (chat_id INTEGER PRIMARY KEY, api_key TEXT, warehouses TEXT, paid INTEGER DEFAULT 0)''')
    conn.commit()
    setup_logger().info(f"Инициализирована таблица users в базе данных {DB}")
    conn.close()
    setup_logger().info(f"Соединение с базой данных {DB} закрыто")
