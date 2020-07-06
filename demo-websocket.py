# -*- coding: utf-8 -*-
import asyncio
import logging
import os

from tock.server import TockServer, TockMode
from tock.websocket import TockWebsocket

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

asyncio.get_event_loop().set_debug(True)

# TockServer(
#     mode=TockMode.WEBSOCKET,
#     apikey=os.environ['TOCK_APIKEY'],
#     host="demo-bot.tock.ai",
#     port=443,
#     protocol="wss"
# )

websocket = TockWebsocket(
    apikey=os.environ['TOCK_APIKEY'],
    host="demo-bot.tock.ai",
    port=443,
    protocol="wss"
)
loop = asyncio.get_event_loop()
loop.run_until_complete(websocket.start())
