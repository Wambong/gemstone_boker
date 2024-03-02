import asyncio
from telegram import Bot

async def send_product_notification(product):
    TELEGRAM_BOT_TOKEN = "6919097745:AAG07P5y7uegerGTrQcA1u7GPT_9gzOicU8"
    chat_id = '5102556482'

    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    message = f"New product added: {product.product_name}\nPrice: {product.price}"

    try:
        await bot.send_message(chat_id=chat_id, text=message)
    except Exception as e:
        print(f"Error sending notification: {e}")



