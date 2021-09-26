from fastapi import HTTPException
from requests import TooManyRedirects, HTTPError

import main
from server.utils.constants import (
    ROOT_MESSAGE,
    EXCEPTION_TooManyRedirects_TEXT,
    EXCEPTION_HTTPError_TEXT
)
from parsing.Parser import Parser
from utils.DataBase import DataBase


class RequestsUtils:
    def __init__(self, url, elems):
        self.site = url
        self.elements = elems
        self.DB = DataBase("My companies")

    def get_info_about_company(self, symbol, query):
        try:
            parser = Parser(symbol, self.site, self.elements)
            result = parser.get_content()

            if query is not None:
                if all(k in result for k in query):
                    result = {key: result[key] for key in query}

        except TooManyRedirects:
            raise HTTPException(status_code=404, detail=EXCEPTION_TooManyRedirects_TEXT)
        except HTTPError:
            raise HTTPException(status_code=500, detail=EXCEPTION_HTTPError_TEXT)

        return result

    def root_func(self):
        return ROOT_MESSAGE

    # now I will have only one DB, but in the future there will be a lot (one for one client)
    # and I will have dict (key: user_ip, value: DB)
    def save_company(self, name, info, user_ip=None):
        # db = get_DB(user_ip)

        # only now, after i'll do it better
        self.DB.add(name, info)

    def del_company(self, name):
        try:
            self.DB.delete(name)
        except KeyError:
            raise HTTPException(status_code=404, detail="{name} not found")

    def kill_bot(self):
        main.kill_bot()
