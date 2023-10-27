import requests
from dotenv import load_dotenv
import os

load_dotenv(os.path.join("", ".env"))

TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def send_telegram_message(text):
    """
    Send a message to a Telegram chat using the provided bot token and chat ID.

    Args:
    - text (str): The message text to send.

    Returns:
    - dict: Response data from the Telegram API.
    """
    response = requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_API_TOKEN}/sendMessage",
        data={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": text
        }
    )
    return response.json()
