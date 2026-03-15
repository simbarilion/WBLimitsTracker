from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, CallbackContext, filters, Application
from .db import init_db
from .logging_config import setup_logger
from .services import get_warehouses, check_limits
from user_repository import get_user, create_user, update_warehouses

logger = setup_logger(__name__)


async def start(update: Update, _: CallbackContext) -> None:
    """Обрабатывает команду /start и проверяет наличие пользователя в базе"""
    if update.effective_chat is None or update.message is None:
        return

    chat_id = update.effective_chat.id
    init_db()
    user = get_user(chat_id)
    if user:
        await update.message.reply_text(
            "Welcome back! Use /check to check limits, /select to change warehouses."
        )
    else:
        await update.message.reply_text(
            "Welcome! Please enter your Wildberries API key to get started."
        )


async def select(update: Update, _: CallbackContext) -> None:
    """Отправляет пользователю список доступных складов для выбора"""
    if update.effective_chat is None or update.message is None:
        return

    chat_id = update.effective_chat.id
    row = get_user(chat_id)
    if not row:
        logger.warning("Установите свой ключ API")
        await update.message.reply_text('Please set your API key first.')
        return
    api_key = row[0]
    warehouses = get_warehouses(api_key)
    if not warehouses:
        await update.message.reply_text('Error fetching warehouses. Check your API key.')
        logger.warning("Установите свой ключ API")
        return
    text = 'Available warehouses:\n'
    for w in warehouses:
        text += f"{w['id']} - {w['name']}\n"
    text += '\nSend comma-separated IDs of warehouses you want to monitor.'
    await update.message.reply_text(text)
    logger.info(f"Отправлен список складов")

async def check(update: Update, _: CallbackContext) -> None:
    """Проверяет лимиты приёмки для выбранных пользователем складов"""
    if update.effective_chat is None or update.message is None:
        return

    chat_id = update.effective_chat.id
    row = get_user(chat_id)
    if not row:
        logger.warning("Выполните настройку с помощью /start")
        await update.message.reply_text('Please setup first with /start.')
        return
    api_key, whs, paid = row
    if not whs:
        await update.message.reply_text('Please select warehouses with /select.')
        logger.warning("Выберите склады с помощью /select")
        return
    msg = check_limits(api_key, whs)
    await update.message.reply_text(msg)
    logger.info(f"Отправлен список остатков по складам")

async def help_command(update: Update, _: CallbackContext) -> None:
    """Отправляет список доступных команд бота"""
    if update.message is None:
        return

    text = (
        "/start - регистрация\n"
        "/select - выбрать склады\n"
        "/check - проверить лимиты\n"
        "/subscribe - подписка\n"
    )
    await update.message.reply_text(text)
    logger.info(f"Отправлен список команд")

async def echo(update: Update, _: CallbackContext) -> None:
    """Повторяет текст сообщения пользователя"""
    if update.message is None:
        return

    await update.message.reply_text(f"Ты написал: {update.message.text}")
    logger.info(f"Отправлено сообщение 'Ты написал: {update.message.text}'")

async def unknown(update: Update, _: CallbackContext) -> None:
    """Обрабатывает неизвестные команды"""
    if update.message is None:
        return

    await update.message.reply_text("Извини, я не знаю такую команду")
    logger.info(f"Отправлено сообщение 'Извини, я не знаю такую команду'")

async def text_handler(update: Update, _: CallbackContext) -> None:
    """Обрабатывает текст пользователя: сохраняет API-ключ или выбранные склады"""
    if update.effective_chat is None or update.message is None:
        return

    chat_id = update.effective_chat.id
    text = update.message.text.strip()
    row = get_user(chat_id)
    if not row:
        create_user(chat_id, text)
        await update.message.reply_text('API key set. Now use /select to choose warehouses.')
        logger.info("Отправлено сообщение 'API-ключ установлен. Используйте /select для выбора складов'")

    elif row[1] == '':
        update_warehouses(chat_id, text)
        await update.message.reply_text('Warehouses selected. Use /check to check limits.')
        logger.info("Отправлено сообщение 'Склад выбран. Используйте /check для отслеживания остатков'")
    else:
        await update.message.reply_text('Unknown input. Use commands.')
        logger.warning("Введена некорректная команда")


def register_handlers(application: Application) -> None:
    """Регистрирует все обработчики команд и сообщений Telegram"""
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("select", select))
    application.add_handler(CommandHandler("check", check))
    application.add_handler(CommandHandler("help", help_command))
    # application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    application.add_handler(MessageHandler(filters.COMMAND, unknown))
