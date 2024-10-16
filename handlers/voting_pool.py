from telegram import Update
from telegram.ext import ContextTypes


voting_pool = {}


async def show_voting_pool(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not voting_pool:
        await update.message.reply_text("هیچ فیلمی در لیست رأی گیری نیست.")
        return

    response_message = "🎥 *فهرست فیلم‌های پیشنهادی برای رأی‌گیری:*\n\n"
    for movie_name, voters in voting_pool.items():
        response_message += f"*فیلم:* {movie_name}\n"
        response_message += (
            f"*رأی‌دهندگان:* {', '.join(voters) if voters else 'هیچ کس'}\n\n"
        )

    await update.message.reply_text(response_message, parse_mode="Markdown")


def add_to_voting_pool(movie_name, username):
    if movie_name not in voting_pool:
        voting_pool[movie_name] = []
    voting_pool[movie_name].append(username)


async def vote_for_movie(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text(
            "لطفا نام فیلمی که می‌خواهید رأی دهید را وارد کنید."
        )
        return

    movie_name = " ".join(context.args)
    username = update.message.from_user.username or "unknown"

    if movie_name not in voting_pool:
        await update.message.reply_text(f"فیلم {movie_name} در لیست رأی گیری نیست.")
        return

    add_to_voting_pool(movie_name, username)
    await update.message.reply_text(f"شما به فیلم *{movie_name}* رأی دادید!")
