# Discord Bot

This is a simple Discord bot created with Python and the `discord.py` library.

## Features

*   Get Pokémon images.
*   Translate text to other languages.
*   Generate fake data (names, addresses).
*   Flip a coin or roll a dice.
*   Welcome new members to the server.
*   Clean messages in a channel.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/your-repository-name.git
    cd your-repository-name
    ```

2.  **Create a virtual environment and activate it:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Create a `.env` file** in the root of the project and add your Discord bot token:
    ```
    TOKEN=your_discord_bot_token
    ```

5.  **Run the bot:**
    ```bash
    python main.py
    ```

## Commands

Here is a list of the available commands:

*   `$poke <pokemon_name>`: Shows the image of the specified Pokémon.
*   `$clean`: Deletes all messages in the current channel.
*   `$translate <language_code> <text>`: Translates the text to the specified language.
*   `$gimme <name|address>`: Generates a fake name or address.
*   `$coin [number_of_flips]`: Flips a coin the specified number of times (default is 1).
*   `$dice [number_of_rolls]`: Rolls a dice the specified number of times (default is 1).

## Dependencies

This project uses the following main libraries:

*   [discord.py](https://discordpy.readthedocs.io/en/stable/): A Python wrapper for the Discord API.
*   [googletrans](https://pypi.org/project/googletrans/): A Python library for using Google Translate.
*   [Faker](https://faker.readthedocs.io/en/master/): A Python package that generates fake data.
*   [Flask](https://flask.palletsprojects.com/en/2.0.x/): A micro web framework for Python.
*   [python-dotenv](https://pypi.org/project/python-dotenv/): Reads key-value pairs from a `.env` file and can set them as environment variables.

For a full list of dependencies, see the `requirements.txt` file.
