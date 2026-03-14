import os
import logging
import datetime
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TELEGRAM_TOKEN:
    raise ValueError("Установи TELEGRAM_TOKEN в переменной окружения!")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бот работает! Введи /help, чтобы узнать команды.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start - запуск\n"
        "/help - помощь\n"
        "/ping - тест ответа\n"
        "/echo <текст> - повторить\n"
        "/sum <a> <b> - сложить числа\n"
        "/menu - показать меню с кнопками\n"
        "/time - текущее время\n"
        "/id - показать твой Telegram ID\n"
    )

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Pong!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        await update.message.reply_text(" ".join(context.args))
    else:
        await update.message.reply_text("Используй: /echo <текст>")

async def sum_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        a, b = map(int, context.args)
        await update.message.reply_text(f"Результат: {a + b}")
    except:
        await update.message.reply_text("Используй: /sum <число1> <число2>")

async def time_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await update.message.reply_text(f"Сейчас: {now}")

async def user_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Твой ID: {update.message.from_user.id}")

async def reply_hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "привет" in update.message.text.lower():
        await update.message.reply_text("Привет")

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Склад", callback_data="warehouse")],
        [InlineKeyboardButton("Статус", callback_data="status")],
    ]
    await update.message.reply_text(
        "Выбери действие:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "warehouse":
        await query.edit_message_text("Список складов пуст (тест)")
    elif query.data == "status":
        await query.edit_message_text("Всё работает")


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logging.error(f"Ошибка: {context.error}")
    if isinstance(update, Update) and update.message:
        await update.message.reply_text("Произошла ошибка, попробуйте ещё раз.")


def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Команды
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("ping", ping))
    application.add_handler(CommandHandler("echo", echo))
    application.add_handler(CommandHandler("sum", sum_command))
    application.add_handler(CommandHandler("menu", menu))
    application.add_handler(CommandHandler("time", time_command))
    application.add_handler(CommandHandler("id", user_id))

    # Текстовые сообщения
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_hello))

    # Кнопки
    application.add_handler(CallbackQueryHandler(button_handler))

    # Ошибки
    application.add_error_handler(error_handler)

    print("Бот запущен в режиме polling...")
    application.run_polling()

if __name__ == "__main__":
    main()
