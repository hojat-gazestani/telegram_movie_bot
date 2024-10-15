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
    await update.message.reply_text('لطفا نام فارسی فیلم را وارد کنید:')
    return MOVIE_NAME

# Collect Persian movie name
async def get_movie_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['movie_name'] = update.message.text
    await update.message.reply_text('لطفا نام انگلیسی فیلم را وارد کنید:')
    return MOVIE_INFO

# Collect English movie name
async def get_movie_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['movie_english_name'] = update.message.text
    await update.message.reply_text('لطفا سال ساخت و کشور سازنده فیلم را وارد کنید:')
    return MOVIE_INFORMATION

# Collect year of production and country
async def get_movie_information(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['movie_year_country'] = update.message.text
    await update.message.reply_text('لطفا نام کارگردان فیلم را وارد کنید:')
    return YOUR_IDEA

# Collect director's name
async def get_your_idea(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['director_name'] = update.message.text
    await update.message.reply_text('لطفا امتیازات فیلم (مثل IMDB) را وارد کنید:')
    return WHY_SUGGEST

# Collect movie ratings
async def get_why_suggest(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['movie_ratings'] = update.message.text
    await update.message.reply_text('مهمترین جایزه دریافتی فیلم را وارد کنید:')
    return MOVIE_PICTURE

# Collect movie awards
async def get_movie_picture(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['movie_awards'] = update.message.text
    await update.message.reply_text('لطفا خلاصه داستان فیلم را بدون اسپویل بنویسید:')
    return WHY_SUGGEST

# Collect plot summary
async def get_plot_summary(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['plot_summary'] = update.message.text
    await update.message.reply_text('چرا این فیلم را پیشنهاد می‌دهید و به نظرتون بعد از دیدن فیلم در چه موضوعاتی میشه صحبت کرد؟')
    return WHY_SUGGEST

# Collect movie picture
async def get_movie_picture(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.photo:
        photo_file = update.message.photo[-1].file_id
        context.user_data['movie_picture'] = photo_file
    else:
        await update.message.reply_text('لطفا یک عکس از فیلم ارسال کنید.')
        return MOVIE_PICTURE

    # Prepare formatted response
    movie_name = context.user_data['movie_name']
    movie_english_name = context.user_data['movie_english_name']
    movie_year_country = context.user_data['movie_year_country']
    director_name = context.user_data['director_name']
    movie_ratings = context.user_data['movie_ratings']
    movie_awards = context.user_data['movie_awards']
    plot_summary = context.user_data['plot_summary']
    why_suggest = context.user_data['why_suggest']
    username = update.message.from_user.username or "unknown"

    response_message = (f"🎬 *Suggested Movie:*\n\n"
                        f"#IntroducedMovie\n\n"
                        f"The user @{username} suggested: \n\n"
                        f"*Persian Name:* {movie_name}\n"
                        f"*English Name:* {movie_english_name}\n"
                        f"*Year & Country:* {movie_year_country}\n"
                        f"*Director:* {director_name}\n"
                        f"*Ratings:* {movie_ratings}\n"
                        f"*Awards:* {movie_awards}\n"
                        f"*Plot Summary:* {plot_summary}\n"
                        f"*Why Suggest:* {why_suggest}\n\n"
                        f"Thank you for your suggestion!")

    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo_file, caption=response_message, parse_mode='Markdown')

    # Clear user data after processing
    context.user_data.clear()

    return ConversationHandler.END

# Handle cancellation
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text('عملیات لغو شد.')
    context.user_data.clear()
    return ConversationHandler.END  # End the conversation

# Responses
def handle_response(text: str) -> str:
    processed: str = text.lower()

    if 'سلام' in processed:
        return 'درود'

    elif 'فیلم' in processed:
        return 'بریم که یه فیلم خوب ببینیم'

    else:
        return 'نمی فهمم چی میگی:)'

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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

if __name__ == '__main__':
    print("Staring bot...")
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('movie', movie_command))
    app.add_handler(CommandHandler('book', book_command))
    app.add_handler(CommandHandler('podcast', podcast_command))

    # Conversation handler for introducing a movie
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('introduce_movie', introduce_movie)],  # Start of the conversation
        states={
            MOVIE_NAME: [MessageHandler(filters.TEXT, get_movie_name)],            # Get Persian movie name
            MOVIE_INFO: [MessageHandler(filters.TEXT, get_movie_info)],            # Get English movie name
            MOVIE_INFORMATION: [MessageHandler(filters.TEXT, get_movie_information)],  # Get year & country
            YOUR_IDEA: [MessageHandler(filters.TEXT, get_your_idea)],              # Get director's name
            WHY_SUGGEST: [MessageHandler(filters.TEXT, get_why_suggest)],          # Get reason for suggestion and discussion topics
            MOVIE_PICTURE: [MessageHandler(filters.PHOTO, get_movie_picture)],     # Get movie picture (photo) in the last step
        },
        fallbacks=[CommandHandler('cancel', cancel)],  # Cancel command as a fallback
    )

    app.add_handler(conv_handler)

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error)

    print('Polling ...')
    app.run_polling(poll_interval=0.5)
