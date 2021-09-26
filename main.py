import os

import uvicorn as uvicorn

import server.main.server_impl as fAPI
from telegram_bot import bot_impl


def get_dir():
    return os.path.dirname(os.path.abspath(__file__))


def kill_bot():
    bot_impl.stop()


def init_fAPI():
    fAPI.init(get_dir())
    uvicorn.run(fAPI.app, host='0.0.0.0', port=8000, lifespan="on")


if __name__ == '__main__':
    bot_impl.init_bot()
    init_fAPI()
