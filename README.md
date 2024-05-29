# Telegraph-Uploader 📤

[![Open Source? Yes!](https://badgen.net/badge/Open%20Source%20%3F/Yes%21/blue?icon=github)](https://github.com/Ns-AnoNymouS/Telegraph-Uploader)
[![Ask Me Anything!](https://img.shields.io/badge/Ask%20me-anything-1abc9c.svg)](https://telegram.dog/Ns_AnoNymouS)

Telegraph-Uploader is a Telegram bot that facilitates the upload of photos to Telegra.ph and generates instant view links for Telegram text messages.

## Features

- **Instant View Links**: Generate instant view links for Telegram text messages. 🔗
- **Photo Uploads**: Upload photos to Telegra.ph and receive a direct link. 🏞

## Easy Deployment

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/Ns-AnoNymouS/Telegraph-Uploader)

1. Obtain your API HASH & API TOKEN from [my.telegram.org](https://my.telegram.org/auth?to=apps)
2. Paste them into their respective fields.
3. Get the bot token from [@BotFather](https://t.me/BotFather).

## How to Run Locally

1. Clone the repository:
    ```sh
    git clone https://github.com/Ns-AnoNymouS/Telegraph-Uploader.git
    cd Telegraph-Uploader
    ```
2. Create virtual environment
    ```sh
    python3 -m venv .venv
    
    # for windows
    .venv\Scripts\activate
    
    # for Linux or MacOS
    source .venv/bin/activate
    ```


3. Install the required libraries:
    ```sh
    pip3 install -r requirements.txt
    ```

4. Add your configuration details to `.env`.
    ```python
    API_HASH = "your_api_hash"
    API_ID = "your_api_id"
    BOT_TOKEN = "your_bot_token"
    ```

5. Run the bot:
    ```sh
    python3 main.py
    ```

## Commands 👨‍✈️

``` 
/start - Check the bot's status and receive instructions on how to use its features.
```

## Usage 🤔

- **Photo Upload**: Send any photo to the bot, and it will return a direct link.
- **Text to Instant View**: Send any text to the bot to generate instant view links.
- **Custom Title**: To use custom title for your post on Telegra.ph, send a text message in the following format:
```
Title: {title}
{content}
```
## Made with 🛠

[Python](https://docs.python.org/)

## Framework 🧰

[Pyrogram](https://docs.pyrogram.org/)

## Developer 👨🏻‍💻

[<img src="https://avatars.githubusercontent.com/u/70622189?v=4" width="100" style="border-radius: 50%" alt="Developer Image">](https://github.com/Ns-AnoNymouS)

**Name**: Anonymous

**GitHub**: [Ns-AnoNymouS](https://github.com/Ns-AnoNymouS)

**Telegram**: [NS AnoNymouS](https://telegram.dog/The_proGrammerr)

## Contributions

Contributions are welcome.
