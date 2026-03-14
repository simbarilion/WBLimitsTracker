import sqlite3
from telegram.ext import CommandHandler, MessageHandler, filters
from .db import init_db
from .logging_config import setup_logger
from .services import get_warehouses, check_limits
from .config import DB

async def start(update, context):
    chat_id = update.effective_chat.id
    init_db()
    conn = sqlite3.connect(DB)
    setup_logger().info(f"Соединение с базой данных {DB} открыто")
    cur = conn.cursor()
    cur.execute('SELECT api_key FROM users WHERE chat_id = ?', (chat_id,))
    if cur.fetchone():
        setup_logger().info(f"Получены данные из базы данных {DB}")
        await update.message.reply_text('Welcome back! Use /check to check limits, /select to change warehouses.')
    else:
        setup_logger().warning("Введите свой API-ключ Wildberries, чтобы начать")
        await update.message.reply_text('Welcome! Please enter your Wildberries API key to get started.')
    conn.close()
    setup_logger().info(f"Соединение с базой данных {DB} закрыто")

async def select(update, context):
    chat_id = update.effective_chat.id
    conn = sqlite3.connect(DB)
    setup_logger().info(f"Соединение с базой данных {DB} открыто")
    cur = conn.cursor()
    cur.execute('SELECT api_key FROM users WHERE chat_id = ?', (chat_id,))
    row = cur.fetchone()
    setup_logger().info(f"Получены данные из базы данных {DB}")
    conn.close()
    setup_logger().info(f"Соединение с базой данных {DB} закрыто")
    if not row:
        setup_logger().warning("Установите свой ключ API")
        await update.message.reply_text('Please set your API key first.')
        return
    api_key = row[0]
    warehouses = get_warehouses(api_key)
    if not warehouses:
        await update.message.reply_text('Error fetching warehouses. Check your API key.')
        setup_logger().warning("Установите свой ключ API")
        return
    text = 'Available warehouses:\n'
    for w in warehouses:
        text += f"{w['id']} - {w['name']}\n"
    text += '\nSend comma-separated IDs of warehouses you want to monitor.'
    await update.message.reply_text(text)
    setup_logger().info(f"Отправлен список складов")

async def check(update, context):
    chat_id = update.effective_chat.id
    conn = sqlite3.connect(DB)
    setup_logger().info(f"Соединение с базой данных {DB} открыто")
    cur = conn.cursor()
    cur.execute('SELECT api_key, warehouses, paid FROM users WHERE chat_id = ?', (chat_id,))
    row = cur.fetchone()
    setup_logger().info(f"Получены данные из базы данных {DB}")
    conn.close()
    setup_logger().info(f"Соединение с базой данных {DB} закрыто")
    if not row:
        setup_logger().warning("Выполните настройку с помощью /start")
        await update.message.reply_text('Please setup first with /start.')
        return
    api_key, whs, paid = row
    if not whs:
        await update.message.reply_text('Please select warehouses with /select.')
        setup_logger().warning("Выберите склады с помощью /select")
        return
    msg = check_limits(api_key, whs)
    await update.message.reply_text(msg)
    setup_logger().info(f"Отправлен список остатков по складам")

async def help_command(update, context):
    text = (
        "/start - регистрация\n"
        "/select - выбрать склады\n"
        "/check - проверить лимиты\n"
        "/subscribe - подписка\n"
    )
    await update.message.reply_text(text)
    setup_logger().info(f"Отправлен список команд")

async def echo(update, context):
    await update.message.reply_text(f"Ты написал: {update.message.text}")
    setup_logger().info(f"Отправлено сообщение 'Ты написал: {update.message.text}'")

async def unknown(update, context):
    await update.message.reply_text("Извини, я не знаю такую команду")
    setup_logger().info(f"Отправлено сообщение 'Извини, я не знаю такую команду'")

async def text_handler(update, context):
    chat_id = update.effective_chat.id
    text = update.message.text.strip()
    conn = sqlite3.connect(DB)
    setup_logger().info(f"Соединение с базой данных {DB} открыто")
    cur = conn.cursor()
    cur.execute('SELECT api_key, warehouses FROM users WHERE chat_id = ?', (chat_id,))
    row = cur.fetchone()
    setup_logger().info(f"Получены данные из базы данных {DB}")
    if not row:
        cur.execute('INSERT INTO users (chat_id, api_key, warehouses, paid) VALUES (?, ?, ?, 0)', (chat_id, text, ''))
        conn.commit()
        setup_logger().info("API - ключ установлен")
        await update.message.reply_text('API key set. Now use /select to choose warehouses.')
        setup_logger().info("Отправлено сообщение 'API-ключ установлен. Используйте /select для выбора складов'")

    elif row[1] == '':
        cur.execute('UPDATE users SET warehouses = ? WHERE chat_id = ?', (text, chat_id))
        conn.commit()
        setup_logger().info("Склад выбран")
        await update.message.reply_text('Warehouses selected. Use /check to check limits.')
        setup_logger().info("Отправлено сообщение 'Склад выбран. Используйте /check для отслеживания остатков'")
    else:
        await update.message.reply_text('Unknown input. Use commands.')
        setup_logger().warning("Введена некорректная команда")
    conn.close()

def register_handlers(application):
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('select', select))
    application.add_handler(CommandHandler('check', check))
    application.add_handler(CommandHandler('help', help_command))
    # application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    application.add_handler(MessageHandler(filters.COMMAND, unknown))
