TELEGRAM_BOT_TOKEN = "6919097745:AAG07P5y7uegerGTrQcA1u7GPT_9gzOicU8"
chat_id = '5102556482'
BOT_USERNAME = "@kudioku_bot"
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler,  ContextTypes, filters, Application

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("hello there how can i help u")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ask me anything")

async def custom_command(update:Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("custom command")

# responds
def handle_response(text):
    processed = text.lower()
    if "hello" in processed:
        return "hi"
    if "how are u" in processed:
        return "i am fine"
    if "what is your name" in processed:
        return "my name is kudioku"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type = update.message.chat.type
    text = update.message.text
    print(f'user ({update.message.chat.id}) in {message_type}: "{text}"')
    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text = text.replace(BOT_USERNAME, '').strip()
            response = handle_response(new_text)
        else:
            return
    else:
        response = handle_response(text)
    print("Bot:", response)
    await update.message.reply_text(response)

async  def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'update {update} caused error {context.error}')

if __name__ == '__main__':
    print('starting bot...')
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("custom", custom_command))

    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    app.add_error_handler(error)
    print('polling')
    app.run_polling(poll_interval=3)