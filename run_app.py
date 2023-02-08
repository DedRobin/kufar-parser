import os
import sys

from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

from services import get_updates, start

BOT_TOKEN = os.environ.get("BOT_TOKEN", None)

if __name__ == "__main__":
    print("cmd entry:", sys.argv)

    application = ApplicationBuilder().token(BOT_TOKEN).build()

    start_handler = CommandHandler("start", start)
    get_updates = MessageHandler(filters.Regex("^Получить объявления$"), get_updates)

    application.add_handler(start_handler)
    application.add_handler(get_updates)

    application.run_polling()
