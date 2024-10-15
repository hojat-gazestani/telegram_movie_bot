from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

MOVIE_NAME_FA, MOVIE_NAME_EN, MOVIE_YEAR, MOVIE_COUNTRY, DIRECTOR_NAME, MOVIE_RATINGS, WHY_SUGGEST, MOVIE_AWARDS, MOVIE_PICTURE = range(9)

async def get_movie_name_fa(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['movie_name_fa'] = update.message.text
    await update.message.reply_text('لطفا نام فارسی فیلم را وارد کنید:')
    return MOVIE_NAME_FA

async def get_movie_name_en(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['movie_name_en'] = update.message.text
    await update.message.reply_text('لطفا نام انگلیسی فیلم را وارد کنید:')
    return MOVIE_NAME_EN

async def get_movie_year(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['movie_year'] = update.message.text
    await update.message.reply_text('لطفا سال ساخت فیلم را وارد کنید:')
    return MOVIE_YEAR

async def get_movie_country(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['movie_country'] = update.message.text
    await update.message.reply_text('لطفا نام کشور سازنده فیلم را وارد کنید:')
    return MOVIE_COUNTRY

async def get_director_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['director_name'] = update.message.text
    await update.message.reply_text('لطفا نام کارگردان فیلم را وارد کنید:')
    return DIRECTOR_NAME

async def get_movie_ratings(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['movie_ratings'] = update.message.text
    await update.message.reply_text('لطفا امتیازات فیلم (مثل IMDB) را وارد کنید:')
    return MOVIE_RATINGS

async def get_why_suggest(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['why_suggest'] = update.message.text
    await update.message.reply_text('مهمترین جایزه دریافتی فیلم را وارد کنید:')
    return MOVIE_AWARDS

async def get_movie_awards(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['movie_awards'] = update.message.text
    await update.message.reply_text('لطفا یک عکس از فیلم ارسال کنید:')
    return MOVIE_PICTURE

async def get_movie_picture(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.photo:
        photo_file = update.message.photo[-1].file_id
        context.user_data['movie_picture'] = photo_file
    else:
        await update.message.reply_text('لطفا یک عکس از فیلم ارسال کنید.')
        return MOVIE_PICTURE

    # Prepare formatted response
    movie_name_fa = context.user_data['movie_name_fa']
    movie_name_en = context.user_data['movie_name_en']
    movie_year = context.user_data['movie_year']
    movie_country = context.user_data['movie_country']
    director_name = context.user_data['director_name']
    movie_ratings = context.user_data['movie_ratings']
    why_suggest = context.user_data['why_suggest']
    movie_awards = context.user_data['movie_awards']
    username = update.message.from_user.username or "unknown"

    response_message = (f"🎬 *Suggested Movie:*\n\n"
                        f"The user @{username} suggested this movie: \n\n"
                        f"*Persian Name:* {movie_name_fa}\n"
                        f"*English Name:* {movie_name_en}\n"
                        f"*Year :* {movie_year}\n"
                        f"*Country:* {movie_country}\n"
                        f"*Director:* {director_name}\n"
                        f"*Ratings:* {movie_ratings}\n"
                        f"*Why Suggested:* {why_suggest}\n"
                        f"*Awards:* {movie_awards}\n")

    await context.bot.send_photo(chat_id=update.effective_chat.id,
                                 photo=photo_file,
                                 caption=response_message,
                                 parse_mode='Markdown')
    context.user_data.clear()
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text('عملیات لغو شد.')
    context.user_data.clear()
    return ConversationHandler.END
