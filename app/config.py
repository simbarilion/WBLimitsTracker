import os

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH_ENV = os.getenv("DB_PATH")
if DB_PATH_ENV:
    DB = os.path.abspath(DB_PATH_ENV)
else:
    DB = os.path.join(BASE_DIR, "database.db")

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

USE_POLLING = os.getenv("USE_POLLING", "1") == "1"

WEBHOOK_URL = f"https://marketai22-kraitens.amvera.io/{TELEGRAM_TOKEN}"
