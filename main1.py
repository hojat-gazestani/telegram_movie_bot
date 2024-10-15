import os
from typing import Final
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    filters,
    ContextTypes,
)

TOKEN: Final = os.getenv("DENALIE_MOVIE_BOT_TOKEN")


(
    MOVIE_NAME_FA,
    MOVIE_NAME_EN,
) = range(2)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("لطفا نام فارسی فیلم را وارد کنید:")
    return MOVIE_NAME_FA


async def get_movie_name_fa(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["movie_name_fa"] = update.message.text
    await update.message.reply_text("لطفا نام انگلیسی فیلم را وارد کنید:")
    return MOVIE_NAME_EN


async def get_movie_name_en(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["movie_name_en"] = update.message.text
    await update.message.reply_text(
        f"thie move name is {context.user_data['movie_name_fa']} and {context.user_data['movie_name_en']}"
    )
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Conversation canceled.")
    return ConversationHandler.END


def main() -> None:
    print("Starting bot...")
    app = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MOVIE_NAME_FA: [MessageHandler(filters.TEXT, get_movie_name_fa)],
            MOVIE_NAME_EN: [MessageHandler(filters.TEXT, get_movie_name_en)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)
    print("Polling ...")
    app.run_polling(poll_interval=0.5)


if __name__ == "__main__":
    main()
