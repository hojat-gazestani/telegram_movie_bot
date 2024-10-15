# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import os
from typing import Final
from telegram import Bot, Update
from telegram.ext import (Application, ApplicationBuilder, CommandHandler, MessageHandler,
                            filters, ContextTypes, ConversationHandler)

# Define conversation states
MOVIE_NAME, MOVIE_INFO, MOVIE_INFORMATION, YOUR_IDEA, WHY_SUGGEST, MOVIE_PICTURE = range(6)


TOKEN: Final = os.getenv("DENALIE_MOVIE_BOT_TEKEN")
BOT_USERNAME: Final = '@denalie_movie_bot'

# Commands
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


# Introduce movie command handler
async def introduce_movie(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text('لطفا نام فیلم را وارد کنید:')
    return MOVIE_NAME


# Collect movie name
async def get_movie_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['movie_name'] = update.message.text
    await update.message.reply_text('لطفا اطلاعات کلی فیلم را وارد کنید:')
    return MOVIE_INFO


# Collect movie info
async def get_movie_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['movie_info'] = update.message.text
    await update.message.reply_text('لطفا اطلاعات بیشتر فیلم را وارد کنید:')
    return MOVIE_INFORMATION


# Collect movie additional information
async def get_movie_information(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['movie_information'] = update.message.text
    await update.message.reply_text('لطفا نظر خود را در مورد این فیلم وارد کنید:')
    return YOUR_IDEA


# Collect user idea
async def get_your_idea(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['your_idea'] = update.message.text
    await update.message.reply_text('لطفا بگویید چرا این فیلم را پیشنهاد می‌کنید:')
    return WHY_SUGGEST


# Collect why to suggest
async def get_why_suggest(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['why_suggest'] = update.message.text

    photo_file = update.message.photo[-1].file_id
    context.user_data['movie_picture'] = photo_file

    username = update.message.from_user.username or "unknown"

    # Format the message
    movie_name = context.user_data['movie_name']
    movie_info = context.user_data['movie_info']
    movie_information = context.user_data['movie_information']
    your_idea = context.user_data['your_idea']
    why_suggest = context.user_data['why_suggest']

    response_message = (f"🎬 *Suggested Movie:*\n\n"
                        f"#IntroducedMovie\n\n"
                        f"The user @{username} suggested: \n\n"
                        f"*Name:* {movie_name}\n"
                        f"*Basic Info:* {movie_info}\n"
                        f"*Additional Info:* {movie_information}\n"
                        f"*Your Idea:* {your_idea}\n"
                        f"*Why Suggest:* {why_suggest}\n\n"
                        f"Thank you for your suggestion!")

    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo_file, caption=response_message, parse_mode='Markdown')


    # Clear user data after processing
    context.user_data.clear()

    return ConversationHandler.END  # End the conversation


# Handle cancellation
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text('عملیات لغو شد.')
    context.user_data.clear()
    return ConversationHandler.END  # End the conversation


# Responses
def handle_response(text: str) -> str:
    proccessed: str = text.lower()

    if 'سلام' in proccessed:
        return  ('درود')

    elif  'فیلم' in proccessed:
        return ('بریم که یه فیلم خوب ببینیم')

    else:
        return ('نمی فهمم چی میگی‌:)')


async  def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message_type = update.message.chat.type
    text = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)

    print('Bot:', response)
    await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Error: {update.message} caused by: {context.error}')

def print_hi(name):

    print(f'Hi, {name}')



if __name__ == '__main__':
    # print_hi('PyCharm')
    print("Staring bot...")
    app = Application.builder().token(TOKEN).build()

    # Cammands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('movie', movie_command))
    app.add_handler(CommandHandler('book', book_command))
    app.add_handler(CommandHandler('podcast', podcast_command))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('introduce_movie', introduce_movie)],
        states={
            MOVIE_PICTURE: [MessageHandler(filters.PHOTO, get_why_suggest)],
            MOVIE_NAME: [MessageHandler(filters.TEXT, get_movie_name)],
            MOVIE_INFO: [MessageHandler(filters.TEXT, get_movie_info)],
            MOVIE_INFORMATION: [MessageHandler(filters.TEXT, get_movie_information)],
            YOUR_IDEA: [MessageHandler(filters.TEXT, get_your_idea)],
            WHY_SUGGEST: [MessageHandler(filters.TEXT, get_why_suggest)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    app.add_handler(conv_handler)

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))


    # Errors
    app.add_error_handler(error)

    print('Polling ...')
    app.run_polling(poll_interval=0.5)
