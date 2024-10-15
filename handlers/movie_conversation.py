from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

MOVIE_NAME, MOVIE_INFO, MOVIE_INFORMATION, YOUR_IDEA, WHY_SUGGEST, MOVIE_PICTURE = range(6)

async def introduce_movie(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text('لطفا نام فارسی فیلم را وارد کنید:')
    return MOVIE_NAME

async def get_movie_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['movie_name'] = update.message.text
    await update.message.reply_text('لطفا نام انگلیسی فیلم را وارد کنید:')
    return MOVIE_INFO

async def get_movie_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['movie_english_name'] = update.message.text
    await update.message.reply_text('لطفا سال ساخت و کشور سازنده فیلم را وارد کنید:')
    return MOVIE_INFORMATION

async def get_movie_information(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['movie_year_country'] = update.message.text
    await update.message.reply_text('لطفا نام کارگردان فیلم را وارد کنید:')
    return YOUR_IDEA

async def get_your_idea(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['director_name'] = update.message.text
    await update.message.reply_text('لطفا امتیازات فیلم (مثل IMDB) را وارد کنید:')
    return WHY_SUGGEST

async def get_why_suggest(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['movie_ratings'] = update.message.text
    await update.message.reply_text('مهمترین جایزه دریافتی فیلم را وارد کنید:')
    return MOVIE_PICTURE

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
    username = update.message.from_user.username or "unknown"

    response_message = (f"🎬 *Suggested Movie:*\n\n"
                        f"The user @{username} suggested: \n\n"
                        f"*Persian Name:* {movie_name}\n"
                        f"*English Name:* {movie_english_name}\n"
                        f"*Year & Country:* {movie_year_country}\n"
                        f"*Director:* {director_name}\n"
                        f"*Ratings:* {movie_ratings}\n"
                        f"*Awards:* {movie_awards}\n")

    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo_file, caption=response_message, parse_mode='Markdown')
    context.user_data.clear()
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text('عملیات لغو شد.')
    context.user_data.clear()
    return ConversationHandler.END
