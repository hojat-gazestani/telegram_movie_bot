import os
from typing import Final

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
    ContextTypes,
)


TOKEN: Final = os.getenv("DENALIE_MOVIE_BOT_TOKEN")
print(TOKEN)

# Define the states
NAME, AGE = range(2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Hi! What's your name?")
    return NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_name = update.message.text
    context.user_data['name'] = user_name  # Store the name
    await update.message.reply_text(f"Nice to meet you, {user_name}! How old are you?")
    return AGE

async def get_age(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_age = update.message.text
    context.user_data['age'] = user_age  # Store the age
    await update.message.reply_text(
        f"Thank you! So you're {context.user_data['name']} and you're {user_age} years old."
    )
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Conversation canceled.")
    return ConversationHandler.END

def main() -> None:
    application = ApplicationBuilder().token("YOUR_BOT_TOKEN").build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_age)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)
    application.run_polling()

if __name__ == '__main__':
    main()

