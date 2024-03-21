import logging
from telegram import Bot
import requests

logger = logging.getLogger(__name__)


def send_notification(message):
    TELEGRAM_BOT_TOKEN = "6919097745:AAG07P5y7uegerGTrQcA1u7GPT_9gzOicU8"
    chat_id = '5102556482'
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    data = {
        'chat_id': chat_id,
        'text': message
    }
    response = requests.post(url, data=data)
    logger.debug(response.text)
    return response.json()

