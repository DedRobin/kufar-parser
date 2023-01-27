import inspect
import logging
import os

import telegram
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from parsers.kufar_parser import parse_kufar

BOT_TOKEN = os.environ.get("BOT_TOKEN", None)
KUFAR_URL = os.environ.get("KUFAR_URL", None)

logger = logging.getLogger(__name__)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
keyboard = [[InlineKeyboardButton('Button: Print Clicked', callback_data=1)], ]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Get products", callback_data='1'),
         ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text('Please choose:', reply_markup=reply_markup)


async def get_products(update: Update, context: ContextTypes.DEFAULT_TYPE):
    first_name = update.effective_chat.first_name
    last_name = update.effective_chat.last_name
    command = inspect.currentframe().f_code.co_name

    logger.info("{0} {1} used command '/{2}'".format(first_name, last_name, command))
    products = parse_kufar(KUFAR_URL)

    for product in products[:1]:
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=product[-1],
            caption="\n".join(product[:-1])
        )


if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    start_handler = CommandHandler('start', start)
    get_products_handler = CommandHandler('get_products', get_products)

    application.add_handler(start_handler)
    application.add_handler(get_products_handler)

    application.run_polling()
