# Telegram Movie Bot

A Telegram bot that allows users to search for and get information about movies. This project is built using Python and utilizes the Telegram Bot API.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Dockerization](#dockerization)
- [Database](#database)
- [License](#license)

## Features

- Search for movies by title
- Get detailed information about a specific movie
- User-friendly interaction via Telegram

## Installation

### Prerequisites

- Python 3.12 or higher
- pip (Python package installer)
- Telegram Bot Token (you can get it by creating a bot with [BotFather](https://core.telegram.org/bots#botfather))

### Clone the repository

```bash
git clone https://github.com/yourusername/telegram_movie_bot.git
cd telegram_movie_bot
```

## Dockerization

To run the bot using Docker:

1. Build the Docker image:
```sh
docker build -t telegram_movie_bot .
```

2. Run the Docker container:
```sh
docker run -d --name telegram_movie_bot telegram_movie_bot
```

3. Run using docker compose:
```sh
docker compose -f docker/docker-compose.yml up -d
```

# License
This project is licensed under the MIT License - see the LICENSE file for details.

```vbnet
### Instructions for Customization

- **Repository Link:** Replace `https://github.com/yourusername/telegram_movie_bot.git` with the actual URL of your GitHub repository.
- **Bot Token:** Ensure that you include instructions on where to find and how to set the bot token.
- **Additional Information:** Add any additional sections or details specific to your project as necessary.

Feel free to modify or expand upon any sections to better fit your project!
```
