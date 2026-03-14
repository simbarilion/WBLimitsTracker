# WB Limits Tracker

**Telegram-бот для мониторинга лимитов отгрузки Wildberries**

Помогает селлерам WB быстро находить бесплатные и дешёвые слоты на складах.  
Бот проверяет коэффициенты приёмки, уведомляет платных пользователей и показывает статус в реальном времени.


## Основные возможности

- Установка API-ключа Wildberries
- Выбор нужных складов для мониторинга
- Проверка текущих лимитов и коэффициентов (`coefficient <= 1` + `allowUnload`)
- Автоматические уведомления каждый час (для платных пользователей)
- Веб-страница статуса (`/`) с количеством пользователей и временем последней проверки
- Поддержка платной подписки (`paid = 1`)

## Технологии

- **Python 3.12**
- **Flask** + **python-telegram-bot**
- **SQLite** (можно легко поменять на PostgreSQL)
- **APScheduler** (фоновые задачи)
- **Poetry** (управление зависимостями)
- **Flake8** + **Black** (стиль кода)

## Запуск приложения

### 1. Клонирование
```bash
git clone https://github.com/simbarilion/wb-limits-tracker.git
cd wb-limits-tracker
```
2. Установка зависимостей
```
poetry install
```
3. Пример настройки окружения
```
FLASK_DEBUG=1
USE_POLLING=1
TELEGRAM_TOKEN=your_telegram_token
DB_PATH=/data/database.db
```
4. Запуск
```
USE_POLLING=0
poetry run python run.py
http://127.0.0.1:5000/

USE_POLLING=1
https://t.me/Marketlimit_bot
```

### Команды бота

/start — начало работы и ввод API-ключа

/select — выбор складов (через запятую ID)

/check — мгновенная проверка лимитов

/help — список команд


## Структура проекта

    ├── app/
    │   ├── bot.py
    │   ├── config.py
    │   ├── db.py
    │   ├── handlers.py
    │   ├── routes.py
    │   ├── scheduler.py
    │   ├── services.py
    │   └── logging_config.py
    ├── run.py
    ├── pyproject.toml
    ├── .env
    └── README.md

### Улучшения

В настоящее время переписываю бот на FastAPI + async + PostgreSQL + Pydantic (полностью асинхронный и production-ready).

### Автор

Надежда Попова

Python Developer

📧 nadezhdapopova13@yandex.ru

🔗 GitHub: simbarilion
