import os

from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler

from services import start, get_updates

BOT_TOKEN = os.environ.get("BOT_TOKEN", None)


if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    start_handler = CommandHandler('start', start)
    get_macbooks_handler = CallbackQueryHandler(get_updates)

    application.add_handler(start_handler)
    application.add_handler(get_macbooks_handler)

    application.run_polling()
