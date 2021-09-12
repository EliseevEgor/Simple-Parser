import requests
from bs4 import BeautifulSoup


class Parser:

    def __init__(self, symbol: str,  site: str, elems):
        url = site + symbol
        req = requests.get(url)
        if req.url != url:
            raise requests.TooManyRedirects()

        req.raise_for_status()

        self.soup = BeautifulSoup(req.text, "html.parser")

        self.__content = {}

        for el in elems["elements"]:
            tag = self.soup.select_one(el["from"])

            if tag is not None:
                self.__content[el["to"]] = tag.get_text()

    def get_content(self):
        return self.__content
