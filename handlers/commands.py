# Commands
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        ["🎬 معرفی فیلم", "📚 معرفی کتاب"],
        ["🎙️ معرفی پادکست", "📜 قوانین گروه"],
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "من ربات گروه فرهنگی دنالی هستم. چطور میتونم کمکت کنم؟",
        reply_markup=reply_markup,
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "از دستورات زیر برای ارتباط با من میتونی استفاده کنی."
    )


async def rule_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        """
    قوانین گروه فرهنگی دنالی
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
