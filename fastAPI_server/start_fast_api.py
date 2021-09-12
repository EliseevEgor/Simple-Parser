import telegram_bot
from parsing.Parser import Parser
from requests import HTTPError, TooManyRedirects
from fastapi import FastAPI, Query, HTTPException
from typing import List, Optional
import json

from fastAPI_server.constants import (
    EXCEPTION_TooManyRedirects_TEXT,
    EXCEPTION_HTTPError_TEXT,
    URL,
    ROOT_MESSAGE,
    CONFIG_PATH,
    PARSE_URL
)

app = FastAPI()
site = URL
elements_to_parsing = {}


def init_elems(root_dir: str):
    with open(root_dir + CONFIG_PATH, 'r+') as f:
        data = f.read()
    global elements_to_parsing
    elements_to_parsing = json.loads(data)


@app.on_event("shutdown")
def shutdown_event():
    telegram_bot.stop()


@app.get("/root")
def root():
    return ROOT_MESSAGE


@app.get(PARSE_URL)
def get_info(symbol, query: Optional[List[str]] = Query(None)):
    try:
        parser = Parser(symbol, site, elements_to_parsing)
        result = parser.get_content()

        if query is not None:
            if all(k in result for k in query):
                result = {key: result[key] for key in query}

    except TooManyRedirects:
        raise HTTPException(status_code=404, detail=EXCEPTION_TooManyRedirects_TEXT)
    except HTTPError:
        raise HTTPException(status_code=500, detail=EXCEPTION_HTTPError_TEXT)

    return result
