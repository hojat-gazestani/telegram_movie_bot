from telegram import Update
from telegram.ext import ContextTypes

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('من ربات گروه فرهنگی دنالی هستم. چطور میتونم کمکت کنم؟')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('از دستورات زیر برای ارتباط با من میتونی استفاده کنی.')

async def movie_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('شروع معرفی فیلم جدید')

async def book_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('شروع معرفی کتاب جدید')

async def podcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('شروع معرفی پادکست جدید')
