import logging
from telegram import Update
from telegram.ext import ContextTypes
import asyncio

logger = logging.getLogger(__name__)


def handle_response(text: str) -> str:
    processed: str = text.lower()

    if "سلام" in processed:
        return "درود"
    elif "فیلم" in processed:
        return "بریم که یه فیلم خوب ببینیم"
    else:
        return "نمی فهمم چی میگی:)"


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message_type = update.message.chat.type
    text = update.message.text

    if message_type == "group" and "@denalie_movie_bot" in text:
        new_text: str = text.replace("@denalie_movie_bot", "").strip()
        response: str = handle_response(new_text)
    else:
        response: str = handle_response(text)

    await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Error: {update.message} caused by: {context.error}")


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error(f"An error occurred: {context.error}")
    await update.message.reply_text("متاسفم، خطایی رخ داده است. لطفاً دوباره تلاش کنید.")
