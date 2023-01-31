import inspect
import logging
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
markup = ReplyKeyboardMarkup(reply_keyboard)


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
    products = parse_kufar()

    for product in products:
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=product[-1],
            caption="\n".join(product[:-1])
        )
