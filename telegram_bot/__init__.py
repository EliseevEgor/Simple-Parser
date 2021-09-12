from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters
)
from telegram_bot.constants import BOT_TOKEN
from telegram_bot.bot_functions import parse_info_from_yahoo, start
import logging

updater = Updater(token=BOT_TOKEN, use_context=True)


def init_bot():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    dispatcher = updater.dispatcher
    """add handler for company's name"""
    echo_handler = MessageHandler(Filters.text & (~Filters.command), parse_info_from_yahoo)
    dispatcher.add_handler(echo_handler)

    """add handler for /start command"""
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    """start telegram bot"""
    updater.start_polling()


def stop():
    updater.stop()


def __init__():
    init_bot()
