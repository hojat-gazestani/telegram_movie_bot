import os
from typing import Final

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    filters,
)

from handlers.movie_conversation import *
from handlers.commands import start_command, rule_command

TOKEN: Final = os.getenv("DENALIE_MOVIE_BOT_TOKEN")


def main() -> None:
    print("Starting bot...")
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("rule", rule_command))
    app.add_handler(CommandHandler("cancel", cancel))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("introduce_movie", introduce_movie)],
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
