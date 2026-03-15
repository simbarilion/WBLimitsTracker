import sqlite3
import os
from .config import DB
from app.logging_config import setup_logger
from contextlib import contextmanager
from typing import Generator


logger = setup_logger(__name__)


@contextmanager
def get_db() -> Generator[sqlite3.Connection, None, None]:
    """Контекстный менеджер для подключения к базе"""
    conn = sqlite3.connect(DB)
    logger.info(f"Соединение с базой данных {DB} открыто")
    try:
        yield conn
    finally:
        conn.close()


def init_db():
    """Инициализирует SQLite базу данных и создаёт таблицу users если не создана"""
    dir_path = os.path.dirname(DB)
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS users
                     (chat_id INTEGER PRIMARY KEY, api_key TEXT, warehouses TEXT, paid INTEGER DEFAULT 0)''')
        conn.commit()
        logger.info(f"Инициализирована таблица users в базе данных {DB}")

