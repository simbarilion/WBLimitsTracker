from typing import Optional, Tuple

from .db import get_db


def get_user(chat_id: int) -> Optional[Tuple]:
    """Возвращает пользователя по chat_id"""
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT api_key, warehouses, paid FROM users WHERE chat_id = ?",
            (chat_id,),
        )
        return cur.fetchone()


def create_user(chat_id: int, api_key: str) -> None:
    """Создаёт нового пользователя"""
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (chat_id, api_key, warehouses, paid) VALUES (?, ?, '', 0)",
            (chat_id, api_key),
        )
        conn.commit()


def update_warehouses(chat_id: int, warehouses: str) -> None:
    """Обновляет список складов пользователя"""
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute(
            "UPDATE users SET warehouses = ? WHERE chat_id = ?",
            (warehouses, chat_id),
        )
        conn.commit()


def get_users() -> list[tuple]:
    """Возвращает всех пользователей"""
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT chat_id, api_key, warehouses, paid FROM users")
        return cur.fetchall()


def get_users_count() -> int:
    """Количество пользователей"""
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM users")
        return cur.fetchone()[0]


def get_paid_users_count() -> int:
    """Количество платных пользователей"""
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM users WHERE paid = 1")
        return cur.fetchone()[0]
