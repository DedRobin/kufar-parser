import inspect
import logging
import shutil
import urllib
import pathlib
import requests

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from parsers.kufar_parser import parse_kufar

logger = logging.getLogger(__name__)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

reply_keyboard = [
    ["Получить объявления"],
]
markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # keyboard = [
    #     [InlineKeyboardButton("Получить последние объявления", callback_data='1'),
    #      ]
    # ]
    first_name = update.effective_chat.first_name
    last_name = update.effective_chat.last_name
    command = inspect.currentframe().f_code.co_name

    logger.info("{0} {1} used command '/{2}'".format(first_name, last_name, command))
    await update.message.reply_text('Выберите действие:', reply_markup=markup)


async def get_updates(update: Update, context: ContextTypes.DEFAULT_TYPE):
    first_name = update.effective_chat.first_name
    last_name = update.effective_chat.last_name
    command = inspect.currentframe().f_code.co_name

    logger.info("{0} {1} used command '/{2}'".format(first_name, last_name, command))

    # products = parse_kufar()
    products = []

    # for product in products:
    for _ in range(1):
        # await context.bot.send_message(chat_id=update.effective_chat.id,
        #                                text=product[0])
        url = 'https://yams.kufar.by/api/v1/kufar-ads/images/88/8823024759.jpg?rule=list_thumbs_2x'
        res = requests.get(url, stream=True)
        with open("test.png", "wb") as f:
            shutil.copyfileobj(res.raw, f)
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            # photo=product[-1],
            photo='https://yams.kufar.by/api/v1/kufar-ads/images/88/8823024759.jpg?rule=list_thumbs_2x',
            # photo=pathlib.Path("test.png"),

            # caption="\n".join(product[:-1]),
        )
        # await asyncio.sleep(0.5)
