import inspect
import logging
import time

from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes

from parsers.kufar_parser import parse_kufar

logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

reply_keyboard = [
    ["Получить объявления"],
]
markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    first_name = update.effective_chat.first_name
    last_name = update.effective_chat.last_name
    command = inspect.currentframe().f_code.co_name

    logger.info("{0} {1} used command '/{2}'".format(first_name, last_name, command))
    await update.message.reply_text("Бот запущен.", reply_markup=markup)


async def get_updates(update: Update, context: ContextTypes.DEFAULT_TYPE):
    start_time = time.time()

    first_name = update.effective_chat.first_name
    last_name = update.effective_chat.last_name
    command = inspect.currentframe().f_code.co_name

    logger.info("{0} {1} used command '/{2}'".format(first_name, last_name, command))

    pages = parse_kufar()
    # url = 'https://yams.kufar.by/api/v1/kufar-ads/images/88/8823024759.jpg?rule=list_thumbs_2x'
    if pages:
        for page in pages:
            for product in page:
                await context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=product[-1],
                    caption="\n".join(product[:-1]),
                )
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="Новых объявлений не найдено"
        )
    end_time = time.time()
    duration = end_time - start_time
    logger.info(f"The command '/{command}' is completed (duration = {duration})")
