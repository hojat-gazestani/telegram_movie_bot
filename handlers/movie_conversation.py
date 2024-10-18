import logging
from telegram import Update
from telegram.ext import (
    ConversationHandler,
    ContextTypes,
)

import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

logger = logging.getLogger(__name__)

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


def is_persian_numeral(num_str):
    """Check if the string contains Persian numerals."""
    persian_numerals = "۰۱۲۳۴۵۶۷۸۹"
    return any(char in persian_numerals for char in num_str)


def convert_persian_to_arabic(num_str):
    """Convert Persian numerals to Arabic numerals."""
    persian_numerals = "۰۱۲۳۴۵۶۷۸۹"
    arabic_numerals = "0123456789"

    translation_table = str.maketrans(persian_numerals, arabic_numerals)
    return num_str.translate(translation_table)


async def save_movie_data(movie_data):
    """Save movie data into the PostgreSQL database."""
    try:

        movie_year = movie_data["movie_year"]
        if is_persian_numeral(movie_year):
            movie_year = convert_persian_to_arabic(movie_year)

        conn = psycopg2.connect(
            host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD
        )
        with conn:
            with conn.cursor() as cursor:
                insert_query = sql.SQL(
                    """
                    INSERT INTO movies (movie_name_fa, movie_name_en, movie_year, movie_country, director_name, movie_ratings, why_suggest, movie_awards)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                )
                cursor.execute(
                    insert_query,
                    (
                        movie_data["movie_name_fa"],
                        movie_data["movie_name_en"],
                        movie_data["movie_year"],
                        movie_data["movie_country"],
                        movie_data["director_name"],
                        movie_data["movie_ratings"],
                        movie_data["why_suggest"],
                        movie_data["movie_awards"],
                    ),
                )
                logger.info("Movie data saved successfully.")
    except Exception as e:
        logger.error(f"Error saving movie data: {e}")
    finally:
        if conn:
            conn.close()


ALLOWED_CHAT_IDS = [-1001151426065, -1001245820221]


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        logger.info(f"User {update.message.from_user.username} canceled the operation.")
        await update.message.reply_text("وارد کردن اطلاعات توسط شما کنسل شد.")
    except Exception as e:
        logger.error(f"Failed to send cancellation message: {e}")
        await update.message.reply_text(
            "متاسفانه، عملیات کنسل نشد. لطفا دوباره تلاش کنید."
        )
    return ConversationHandler.END


async def introduce_movie(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    # if update.message.chat_id != ALLOWED_CHAT_IDS:
    #    logger.warning(
    #        f"Unauthorized access attempt from chat: {update.message.chat_id}"
    #    )
    #    await update.message.reply_text(
    #        "با حجت تماس بگیرید.  شما به این بات دسترسی ندارید."
    #    )
    #    return ConversationHandler.END

    logger.info(
        f"User {update.message.from_user.username} started introducing a movie."
    )
    await update.message.reply_text("لطفا نام فارسی فیلم را وارد کنید:")
    return MOVIE_NAME_FA


async def get_movie_name_fa(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        movie_name_fa = update.message.text
        logger.info(f"Received movie name (FA): {movie_name_fa}")
        context.user_data["movie_name_fa"] = movie_name_fa
        await update.message.reply_text("لطفا نام انگلیسی فیلم را وارد کنید:")
        return MOVIE_NAME_EN
    except Exception as e:
        logger.error(f"Error in getting movie name (FA): {e}")
        await update.message.reply_text(
            "متاسفانه، در دریافت نام فیلم فارسی مشکلی پیش آمد. لطفا دوباره تلاش کنید."
        )
        return MOVIE_NAME_FA


async def get_movie_name_en(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        movie_name_en = update.message.text
        logger.info(f"Received movie name (EN): {movie_name_en}")
        context.user_data["movie_name_en"] = movie_name_en
        await update.message.reply_text("لطفا سال ساخت فیلم را وارد کنید:")
        return MOVIE_YEAR
    except Exception as e:
        logger.error(f"Error in getting movie name (EN): {e}")
        await update.message.reply_text(
            "متاسفانه، در دریافت نام انگلیسی فیلم مشکلی پیش آمد. لطفا دوباره تلاش کنید."
        )
        return MOVIE_NAME_EN


async def get_movie_year(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        movie_year = update.message.text
        if not movie_year.isdigit() or not (1000 <= int(movie_year) <= 3000):
            raise ValueError("Invalid year format")
        context.user_data["movie_year"] = movie_year
        logger.info(
            f"User {update.message.from_user.username} entered movie year: {movie_year}"
        )
        await update.message.reply_text("لطفا نام کشور سازنده فیلم را وارد کنید:")
        return MOVIE_COUNTRY
    except ValueError:
        await update.message.reply_text(
            "لطفا سال ساخت را به درستی وارد کنید (مثلاً 2020):"
        )
        return MOVIE_YEAR  # Retry the same step
    except Exception as e:
        logger.error(f"Error in getting movie year: {e}")
        await update.message.reply_text(
            "متاسفانه، در دریافت سال ساخت فیلم مشکلی پیش آمد. لطفا دوباره تلاش کنید."
        )
        return MOVIE_YEAR


async def get_movie_country(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        movie_country = update.message.text
        context.user_data["movie_country"] = movie_country
        logger.info(
            f"User {update.message.from_user.username} entered movie country: {movie_country}"
        )
        await update.message.reply_text("لطفا نام کارگردان فیلم را وارد کنید:")
        return DIRECTOR_NAME
    except Exception as e:
        logger.error(f"Error in getting movie country: {e}")
        await update.message.reply_text(
            "متاسفانه، در دریافت کشور سازنده فیلم مشکلی پیش آمد. لطفا دوباره تلاش کنید."
        )
        return MOVIE_COUNTRY


async def get_director_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        director_name = update.message.text
        context.user_data["director_name"] = director_name
        logger.info(
            f"User {update.message.from_user.username} entered director name: {director_name}"
        )
        await update.message.reply_text("لطفا امتیازات فیلم (مثل IMDB) را وارد کنید:")
        return MOVIE_RATINGS
    except Exception as e:
        logger.error(f"Error in getting director name: {e}")
        await update.message.reply_text(
            "متاسفانه، در دریافت نام کارگردان فیلم مشکلی پیش آمد. لطفا دوباره تلاش کنید."
        )
        return DIRECTOR_NAME


async def get_movie_ratings(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    movie_ratings = update.message.text
    context.user_data["movie_ratings"] = movie_ratings
    logger.info(
        f"User {update.message.from_user.username} entered movie ratings: {movie_ratings}"
    )
    await update.message.reply_text(
        "نظر شخصی شما و دلیل پیشنهاد فیلم و اینکه به نظرت بعد از فیلم میشه در چه موردهایی صحبت و تبادل نظر کرد.:"
    )
    return WHY_SUGGEST


async def get_why_suggest(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        why_suggest = update.message.text
        context.user_data["why_suggest"] = why_suggest
        logger.info(
            f"User {update.message.from_user.username} entered reason for suggestion: {why_suggest}"
        )
        await update.message.reply_text("مهمترین جایزه دریافتی فیلم را وارد کنید:")
        return MOVIE_AWARDS
    except Exception as e:
        logger.error(f"Error in getting why suggest: {e}")
        await update.message.reply_text(
            "متاسفانه، در دریافت دلیل پیشنهاد فیلم مشکلی پیش آمد. لطفا دوباره تلاش کنید."
        )
        return WHY_SUGGEST


async def get_movie_awards(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        movie_awards = update.message.text
        context.user_data["movie_awards"] = movie_awards
        logger.info(
            f"User {update.message.from_user.username} entered movie awards: {movie_awards}"
        )
        await update.message.reply_text("لطفا یک عکس از فیلم ارسال کنید.")
        return MOVIE_PICTURE
    except Exception as e:
        logger.error(f"Error in getting movie awards: {e}")
        await update.message.reply_text(
            "متاسفانه، در دریافت یک عکس از فیلم مشکلی پیش آمد. لطفا دوباره تلاش کنید."
        )
        return MOVIE_PICTURE


async def get_movie_picture(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.photo:

        photo_file = update.message.photo[-1].file_id
        context.user_data["movie_picture"] = photo_file

        username = update.message.from_user.username or "unknown"
        logger.info(f"User {username} uploaded a movie picture")

        movie_data = {
            "movie_name_fa": context.user_data["movie_name_fa"],
            "movie_name_en": context.user_data["movie_name_en"],
            "movie_year": context.user_data["movie_year"],
            "movie_country": context.user_data["movie_country"],
            "director_name": context.user_data["director_name"],
            "movie_ratings": context.user_data["movie_ratings"],
            "why_suggest": context.user_data["why_suggest"],
            "movie_awards": context.user_data["movie_awards"],
            "movie_picture": photo_file,
        }

        await save_movie_data(movie_data)

        response_message = (
            f"🎬 *#پیشنهادفیلم :*\n\n"
            f"*ایشون* @{username} فیلم زیر را پیشنهاد داده: \n\n"
            f"*نام فارسی:*  {movie_data['movie_name_fa']}\n"
            f"*نام انگلیسی:* {movie_data['movie_name_en']}\n"
            f"*سال ساخت :* {movie_data['movie_year']}\n"
            f"*کشور سازنده:* {movie_data['movie_country']}\n"
            f"*کارگردان:* {movie_data['director_name']}\n"
            f"*امتیازات:* {movie_data['movie_ratings']}\n"
            f"*جوایز:* {movie_data['movie_awards']}\n"
            f"* \n نظر شخصی و دلیل پیشنهاد\n:* {movie_data['why_suggest']}\n"
        )

        logger.info(f"Movie introduced: ({movie_data['movie_name_en']}) by {username}")

        try:
            await context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=photo_file,
                caption=response_message[:1024],
                parse_mode="Markdown",
            )
            logger.info(
                f"Movie suggestion conversation with {username} ended successfully."
            )
            context.user_data.clear()
            return ConversationHandler.END
        except Exception as e:
            logger.error(f"Failed to send photo: {e}")
            await update.message.reply_text(
                "متاسفانه، ارسال عکس با خطا مواجه شد. لطفا دوباره تلاش کنید."
            )
            return MOVIE_PICTURE

    else:
        logger.warning(f"No photo received from {update.message.from_user.username}")
        await update.message.reply_text("لطفا یک عکس از فیلم ارسال کنید.")
        return MOVIE_PICTURE
