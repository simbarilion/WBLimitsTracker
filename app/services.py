from typing import Dict, List, Optional

import requests

from app.logging_config import setup_logger

logger = setup_logger(__name__)


def get_warehouses(api_key: str) -> Optional[List[Dict]]:
    """Получает список складов продавца из API Wildberries"""
    url = "https://suppliers-api.wildberries.ru/api/v1/warehouses"
    headers = {"Authorization": api_key}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        logger.info("GET-запрос успешно обработан")
        result = r.json()
        logger.info("Данные преобразованы в json-формат")
        return result
    except Exception as e:
        logger.error(f"Ошибка при загрузке складов: {e}")
        return None


def check_limits(api_key: str, warehouse_ids: str) -> str:
    """Проверяет коэффициенты приёмки по выбранным складам Wildberries"""
    if not warehouse_ids:
        logger.warning("Склады не выбраны")
        return "No warehouses selected"
    url = f"https://suppliers-api.wildberries.ru/api/v1/acceptance/coefficients?warehouseIDs={warehouse_ids}"
    headers = {"Authorization": api_key}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        logger.info("GET-запрос успешно обработан")
        data = r.json()
        logger.info("Данные преобразованы в json-формат")
        available = []
        for item in data:
            if item.get("coefficient", 999) <= 1 and item.get("allowUnload", False):
                available.append(
                    f"Warehouse {item['warehouseID']} on {item['date']}: coefficient {item['coefficient']}"
                )
        return (
            "Available free/cheap limits:\n" + "\n".join(available)
            if available
            else "No available free/cheap limits currently."
        )
    except Exception as e:
        logger.error(f"Ошибка проверки лимитов: {e}")
        return f"Error checking limits: {str(e)}"
