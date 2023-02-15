import sys, os

from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

from bots.services import get_updates, start
from settings import BOT_TOKEN, logger

if __name__ == "__main__":
    try:
        arg = sys.argv[1]
    except IndexError:
        pass
    else:
        if arg == "clear_cache":
            os.remove("cache.txt")
            logger.info("Cache has been clear")

    application = ApplicationBuilder().token(BOT_TOKEN).build()

    start_handler = CommandHandler("start", start)
    get_updates = MessageHandler(filters.Regex("^Получить объявления$"), get_updates)

    application.add_handler(start_handler)
    application.add_handler(get_updates)

    application.run_polling()
