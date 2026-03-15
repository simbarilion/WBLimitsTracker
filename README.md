# WB Limits Tracker

**Телеграм-бот для отслеживания лимитов приёмки на Wildberries**

Позволяет пользователям регистрироваться, выбирать склады и получать уведомления о доступных лимитах.

## Основные возможности

- Регистрация и управление API-ключом Wildberries
- Выбор складов для мониторинга
- Проверка доступных лимитов через команду /check
- Автоматическая проверка лимитов с уведомлением пользователей
- Веб-интерфейс для просмотра статистики (общее количество пользователей, платные пользователи, 
последнее выполнение scheduler)
- Логирование действий и ошибок

## Технологии

- **Python 3.12**
- **Flask** для веб-интерфейса и webhook
- **python-telegram-bot v20+**
- **SQLite** для хранения пользователей
- **APScheduler** для периодических задач
- **requests** для взаимодействия с API Wildberries

## Установка

### 1. Клонируем репозиторий:
```bash
git clone https://github.com/simbarilion/wb-limits-tracker.git
cd wb-limits-tracker
```

2. Создаём и активируем виртуальное окружение:
```
python -m venv .venv
source .venv/bin/activate  # Linux / Mac
.venv\Scripts\activate     # Windows
```

3. Устанавливаем зависимости:
```
pip install -r requirements.txt

через poetry:
poetry install
```

4. Создаём файл .env в корне проекта:
```
USE_POLLING=1
TELEGRAM_TOKEN=your_telegram_token
DB_PATH=./database.db
```
4. Запуск
```
Режим webhook:
USE_POLLING=0
python run.py
http://127.0.0.1:5000/

Режим polling (для локальной разработки):
USE_POLLING=1
python run.py
https://t.me/Marketlimit_bot
```

### Команды бота

/start — Регистрация пользователя и установка API-ключа

/select — Выбор складов для мониторинга

/check — Проверка лимитов выбранных складов

/help — Показать все доступные команды

## Структура проекта

    app/
    ├─ bot.py              # Инициализация бота и Application
    ├─ handlers.py         # Обработчики команд Telegram
    ├─ user_repository.py  # Работа с базой пользователей (CRUD)
    ├─ services.py         # Работа с API Wildberries
    ├─ db.py               # Инициализация SQLite + контекстный менеджер
    ├─ scheduler.py        # Планировщик регулярной проверки лимитов
    ├─ routes.py           # Flask Blueprint + HTML templates
    ├─ config.py           # Конфигурация проекта (.env)
    ├─ logging_config.py   # Настройка логирования
    ├─ templates/
    │  └─ index.html       # Веб-шаблон для страницы статуса
    └─ __init__.py         # Создание Flask-приложения
    run.py                 # Точка входа приложения
    pyproject.toml
    .env
    README.md

### Логи

- Все действия и ошибки логируются в папку logs/.

- Можно выводить логи в консоль через log_to_console=True.

### Улучшения

В настоящее время переписываю бот на FastAPI + async + PostgreSQL + Pydantic

### Автор

Надежда Попова

Python Developer

📧 nadezhdapopova13@yandex.ru

🔗 GitHub: simbarilion
