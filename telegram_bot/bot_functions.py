import json

from fastapi import HTTPException

from DB.companies import database
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


def add_company_to_BD(user_id, name):
    return database.add_company(user_id, name, "COMPANIES")


def delete_company_from_BD(user_id, name):
    return database.delete_company(user_id, name, "COMPANIES")


def show_companies(user_id):
    return database.get_companies(user_id, "COMPANIES")


def parse_client_command(update, context):
    username = update.message['chat']['id']
    text: str = update.message.text
    text = text.lower()
    if text.startswith("добавь компанию "):
        words = text.split(" ")
        name = words[len(words) - 1]
        result = add_company_to_BD(username, name)
        context.bot.send_message(chat_id=update.effective_chat.id, text=result)
    elif text.startswith("удали компанию "):
        words = text.split(" ")
        name = words[len(words) - 1]
        result = delete_company_from_BD(username, name)
        context.bot.send_message(chat_id=update.effective_chat.id, text=result)
    elif text.startswith("покажи мои компании"):
        result = show_companies(username)
        context.bot.send_message(chat_id=update.effective_chat.id, text=result)
    else:
        parse_info_from_yahoo(update, context)


def parse_info_from_yahoo(update, context):
    from server.main.server_impl import get_info
    try:
        ans = get_info(update.message.text, None)
    except HTTPException as e:
        if e.detail == EXCEPTION_TooManyRedirects_TEXT:
            send_message(update, context, EXCEPTION_CANT_FIND)
        else:
            send_message(update, context, EXCEPTION_ALL_ELSE)
        print("Exception: code = " + str(e.status_code) + " Details - " + e.detail)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=json.dumps(ans, indent=2))
