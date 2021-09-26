from pydantic import BaseModel

from server.main.request_utils import RequestsUtils
from fastapi import FastAPI, Query
from typing import List, Optional
import json

from server.utils.constants import (
    URL,
    CONFIG_PATH,
    PARSE_URL
)

app = FastAPI()
request_func: RequestsUtils


def init(root_dir: str):
    with open(root_dir + CONFIG_PATH, 'r+') as f:
        data = f.read()
    global request_func
    request_func = RequestsUtils(URL, json.loads(data))


@app.on_event("shutdown")
def shutdown_event():
    request_func.kill_bot()
    return {"msg": "success"}


@app.get("/root")
def root():
    return request_func.root_func()


class Company(BaseModel):
    name: str
    symbol: str
    fields: Optional[list[str]] = None


# get info about company
# plus save this info to db
@app.post("/companies/", status_code=200)
def save_info_about_company(c: Company):
    res = request_func.get_info_about_company(c.symbol, c.fields)
    request_func.save_company(c.name, res)
    return c


# delete info about company
@app.delete("/companies/", status_code=200)
def delete_company(c: Company):
    request_func.del_company(c.name)
    return c


@app.get(PARSE_URL)
def get_info(symbol, query: Optional[List[str]] = Query(None)):
    return request_func.get_info_about_company(symbol, query)
