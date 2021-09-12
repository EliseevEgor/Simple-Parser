import os

import uvicorn as uvicorn

import telegram_bot
import fastAPI_server.start_fast_api as fAPI

if __name__ == '__main__':
    telegram_bot.__init__()
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    fAPI.init_elems(ROOT_DIR)
    uvicorn.run(fAPI.app, host='0.0.0.0', port=8000, lifespan="on")
