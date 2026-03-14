import sqlite3
from datetime import datetime
from flask import Blueprint, request
import telegram

from .config import TELEGRAM_TOKEN, WEBHOOK_URL, DB
from .logging_config import setup_logger
from .scheduler import last_run_time
from .bot import application

bp = Blueprint("routes", __name__)

bot = telegram.Bot(token=TELEGRAM_TOKEN)

@bp.route(f"/{TELEGRAM_TOKEN}", methods=["POST"])
def webhook():
    try:
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        application.update_queue.put_nowait(update)
        return "ok", 200
    except Exception as e:
        setup_logger().error(f"Ошибка webhook: {e}")
        return f"error: {e}", 500

@bp.route('/set_webhook', methods=['GET'])
def set_webhook():
    try:
        bot.set_webhook(url=WEBHOOK_URL, drop_pending_updates=True)
        return "Webhook setup ok"
    except Exception as e:
        setup_logger().error(f"Ошибка установки webhook: {e}")
        return f"Webhook setup failed: {e}"

@bp.route('/')
def index():
    conn = sqlite3.connect(DB)
    setup_logger().info(f"Соединение с базой данных {DB} открыто")
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM users")
    setup_logger().info(f"Получено количество пользователей")
    total_users = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM users WHERE paid = 1")
    setup_logger().info(f"Получено количество пользователей со статусом paid")
    paid_users = cur.fetchone()[0]
    conn.close()

    last_check = last_run_time.strftime('%Y-%m-%d %H:%M:%S') if last_run_time else "ещё не запускался"

    html = f"""
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <title>Bot Status</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
      </head>
      <body class="p-4">
        <div class="container">
          <h2 class="mb-4">🤖 Bot Status</h2>
          <div class="card p-3 shadow-sm">
            <p><b>Status:</b> <span class="text-success">Online</span></p>
            <p><b>Total users:</b> {total_users}</p>
            <p><b>Paid users:</b> {paid_users}</p>
            <p><b>Last scheduler run:</b> {last_check}</p>
            <p><b>Last check:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
          </div>
        </div>
      </body>
    </html>
    """
    return html
