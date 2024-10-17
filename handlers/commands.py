# Commands
import os
from typing import Final

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

from handlers.utils import handle_response

BOT_USERNAME: Final = os.getenv("BOT_USERNAME")


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        ["🎬 معرفی فیلم", "📚 معرفی کتاب"],
        ["🎙️ معرفی پادکست", "📜 قوانین گروه"],
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        """من ربات گروه فرهنگی دنالی هستم. چطور میتونم کمکت کنم؟
        در هر مرحله ایی میتوانید با /cancel کنسل کنید

        """,
        reply_markup=reply_markup,
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "از دستورات زیر برای ارتباط با من میتونی استفاده کنی."
    )


async def rule_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        """
    قوانین معرفی فیلم:
    ۱. حتما فیلمی معرفی کنید که شخصا دیده باشید
    ۲. در صورتی که وارد لیست سیاه شوید دیگر امکان پیشنهاد فیلم برای شما وجود نخواهد داشت
"""
    )


async def movie_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("شروع معرفی فیلم جدید")


async def book_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("شروع معرفی کتاب جدید")


async def podcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("شروع معرفی پادکست جدید")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message_type = update.message.chat.type
    text = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == "group":
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, "").strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)

    print("Bot:", response)
    await update.message.reply_text(response)
