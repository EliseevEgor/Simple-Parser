import json

from fastapi import HTTPException

from telegram_bot.constants import (
    HELLO_MESSAGE,
    EXCEPTION_CANT_FIND,
    EXCEPTION_ALL_ELSE
)
from server.utils.constants import (
    EXCEPTION_TooManyRedirects_TEXT,
)


def send_message(update, context, text: str):
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def start(update, context):
    send_message(update, context, text=HELLO_MESSAGE)


def parse_info_from_yahoo(update, context):
    from server.main.server_impl import get_info
    try:
        # пока что None, чуть позже сделаю нормально
        ans = get_info(update.message.text, None)
    except HTTPException as e:
        if e.detail == EXCEPTION_TooManyRedirects_TEXT:
            send_message(update, context, EXCEPTION_CANT_FIND)
        else:
            send_message(update, context, EXCEPTION_ALL_ELSE)
        print("Exception: code = " + str(e.status_code) + " Details - " + e.detail)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=json.dumps(ans, indent=2))
