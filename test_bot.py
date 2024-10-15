import os
from typing import Final
from telegram import Bot


TOKEN: Final = os.getenv("DENALIE_MOVIE_BOT_TEKEN")
BOT_USERNAME: Final = '@denalie_movie_bot'

async def main():
    bot = Bot(token=TOKEN)

    bot_username = bot.get_me().username
    print(f"Bot username: {bot_username}")

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())