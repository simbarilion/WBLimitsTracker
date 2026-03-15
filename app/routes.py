from datetime import datetime
from flask import Blueprint, request, render_template
import telegram

from .config import TELEGRAM_TOKEN, WEBHOOK_URL
from .logging_config import setup_logger
from .scheduler import last_run_time
from .bot import application
from .user_repository import get_users_count, get_paid_users_count

logger = setup_logger(__name__)

bp = Blueprint("routes", __name__, template_folder="templates")

bot = telegram.Bot(token=TELEGRAM_TOKEN)

@bp.route(f"/{TELEGRAM_TOKEN}", methods=["POST"])
def webhook():
    """Принимает webhook обновления от Telegram и передаёт их боту"""
    try:
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        application.update_queue.put_nowait(update)
        return "ok", 200
    except Exception as e:
        logger.error(f"Ошибка webhook: {e}")
        return f"error: {e}", 500

@bp.route("/set_webhook", methods=["GET"])
def set_webhook():
    """Устанавливает webhook для Telegram-бота"""
    try:
        bot.set_webhook(url=WEBHOOK_URL, drop_pending_updates=True)
        return "Webhook setup ok"
    except Exception as e:
        logger.error(f"Ошибка установки webhook: {e}")
        return f"Webhook setup failed: {e}"

@bp.route("/")
def index():
    """Отображает страницу статуса бота и статистику пользователей"""
    total_users = get_users_count()
    paid_users = get_paid_users_count()
    last_check = last_run_time.strftime('%Y-%m-%d %H:%M:%S') if last_run_time else "ещё не запускался"

    return render_template(
        "index.html",
        total_users=total_users,
        paid_users=paid_users,
        last_run=last_check,
        now=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )
