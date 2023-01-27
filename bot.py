import logging
import os
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes

from parsers.kufar_parser import parse_kufar

BOT_TOKEN = os.environ.get("BOT_TOKEN", None)
KUFAR_URL = os.environ.get("KUFAR_URL", None)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)


async def get_products(update: Update, context: ContextTypes.DEFAULT_TYPE):
    products = parse_kufar(KUFAR_URL)
    products = [", ".join(p) for p in products[:-1]]

    # file = open("image.png", "rb")

    for product in products:
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            # photo=
            )
        # await context.bot.send_message(chat_id=update.effective_chat.id, text=product)


if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    caps_handler = CommandHandler('caps', caps)
    get_products_handler = CommandHandler('get_products', get_products)

    application.add_handler(start_handler)
    application.add_handler(echo_handler)
    application.add_handler(caps_handler)
    # application.add_handler(get_products_handler)

    application.run_polling()
