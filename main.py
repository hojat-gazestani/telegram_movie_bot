import os
from typing import Final
from telegram.ext import Application, CommandHandler, MessageHandler, ConversationHandler, filters
from handlers.commands import start_command, help_command, movie_command, book_command, podcast_command
from handlers.movie_conversation import introduce_movie, get_movie_name, get_movie_info, get_movie_information, get_your_idea, get_why_suggest, get_movie_picture, cancel
from handlers.utils import handle_message, error

TOKEN: Final = os.getenv("DENALIE_MOVIE_BOT_TEKEN")

if __name__ == '__main__':
    print("Starting bot...")
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('movie', movie_command))
    app.add_handler(CommandHandler('book', book_command))
    app.add_handler(CommandHandler('podcast', podcast_command))

    # Conversation handler for introducing a movie
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('introduce_movie', introduce_movie)],
        states={
            0: [MessageHandler(filters.TEXT, get_movie_name)],
            1: [MessageHandler(filters.TEXT, get_movie_info)],
            2: [MessageHandler(filters.TEXT, get_movie_information)],
            3: [MessageHandler(filters.TEXT, get_your_idea)],
            4: [MessageHandler(filters.TEXT, get_why_suggest)],
            5: [MessageHandler(filters.PHOTO, get_movie_picture)],
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
