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
    MOVIE_YEAR,
    MOVIE_COUNTRY,
    DIRECTOR_NAME,
    MOVIE_RATINGS,
    WHY_SUGGEST,
    MOVIE_AWARDS,
    MOVIE_PICTURE,
) = range(9)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("لطفا نام فارسی فیلم را وارد کنید:")
    return MOVIE_NAME_FA


async def get_movie_name_fa(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["movie_name_fa"] = update.message.text
    await update.message.reply_text("لطفا نام انگلیسی فیلم را وارد کنید:")
    return MOVIE_NAME_EN


async def get_movie_name_en(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["movie_name_en"] = update.message.text
    await update.message.reply_text("لطفا سال ساخت فیلم را وارد کنید:")
    return MOVIE_YEAR


async def get_movie_year(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["movie_year"] = update.message.text
    await update.message.reply_text("لطفا نام کشور سازنده فیلم را وارد کنید:")
    return MOVIE_COUNTRY


async def get_movie_country(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["movie_country"] = update.message.text
    await update.message.reply_text("لطفا نام کارگردان فیلم را وارد کنید:")
    return DIRECTOR_NAME


async def get_director_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["director_name"] = update.message.text
    await update.message.reply_text("لطفا امتیازات فیلم (مثل IMDB) را وارد کنید:")
    return MOVIE_RATINGS


async def get_movie_ratings(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["movie_ratings"] = update.message.text
    await update.message.reply_text(
        "نظر شخصی شما و دللیل پیشنهاد فیلم و اینکه به نظرت بعد از فیلم میشه در چه موردهایی صحبت و تبادل نظر کرد.:"
    )
    return WHY_SUGGEST


async def get_why_suggest(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["why_suggest"] = update.message.text
    await update.message.reply_text("مهمترین جایزه دریافتی فیلم را وارد کنید:")
    return MOVIE_AWARDS


async def get_movie_awards(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["movie_awards"] = update.message.text
    await update.message.reply_text("لطفا یک عکس از فیلم ارسال کنید.")
    return MOVIE_PICTURE


async def get_movie_picture(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    photo_file = update.message.photo[-1].file_id
    context.user_data["movie_picture"] = photo_file

    username = update.message.from_user.username or "unknown"

    # Prepare formatted response
    movie_name_fa = context.user_data["movie_name_fa"]
    movie_name_en = context.user_data["movie_name_en"]
    movie_year = context.user_data["movie_year"]
    movie_country = context.user_data["movie_country"]
    director_name = context.user_data["director_name"]
    movie_ratings = context.user_data["movie_ratings"]
    why_suggest = context.user_data["why_suggest"]
    movie_awards = context.user_data["movie_awards"]

    response_message = (
        f"🎬 *#پیشنهادفیلم :*\n\n"
        f"جناب @{username} فیلم زیر را پیشنهاد داده: \n\n"
        f"*نام فارسی:* {movie_name_fa}\n"
        f"*نام انگلیسی:* {movie_name_en}\n"
        f"*سال ساخت :* {movie_year}\n"
        f"*کشور سازنده:* {movie_country}\n"
        f"*کارگردان:* {director_name}\n"
        f"*امتیازات:* {movie_ratings}\n"
        f"*جوایز:* {movie_awards}\n"
        f"*نظر شخصی و دلیل پیشنهاد:* {why_suggest}\n"
    )

    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=photo_file,
        caption=response_message,
        parse_mode="Markdown",
    )
    context.user_data.clear()
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("عملیات لغو شد.")
    return ConversationHandler.END


def main() -> None:
    print("Starting bot...")
    app = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MOVIE_NAME_FA: [MessageHandler(filters.TEXT, get_movie_name_fa)],
            MOVIE_NAME_EN: [MessageHandler(filters.TEXT, get_movie_name_en)],
            MOVIE_YEAR: [MessageHandler(filters.TEXT, get_movie_year)],
            MOVIE_COUNTRY: [MessageHandler(filters.TEXT, get_movie_country)],
            DIRECTOR_NAME: [MessageHandler(filters.TEXT, get_director_name)],
            MOVIE_RATINGS: [MessageHandler(filters.TEXT, get_movie_ratings)],
            WHY_SUGGEST: [MessageHandler(filters.TEXT, get_why_suggest)],
            MOVIE_AWARDS: [MessageHandler(filters.TEXT, get_movie_awards)],
            MOVIE_PICTURE: [MessageHandler(filters.PHOTO, get_movie_picture)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)
    print("Polling ...")
    app.run_polling(poll_interval=0.5)


if __name__ == "__main__":
    main()
