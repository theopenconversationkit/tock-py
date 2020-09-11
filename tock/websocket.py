# -*- coding: utf-8 -*-
import json
import logging
import sys
from json import JSONDecodeError
from typing import Callable

import aiohttp

from tock.models import TockMessage
from tock.schemas import TockMessageSchema


class TockWebsocket:
    """
    Tock Web Socket mode
    """

    def __init__(
            self,
            apikey: str = "apikey_is_undefined",
            host: str = "demo-bot.tock.ai",
            port: int = 443,
            protocol: str = "wss",
            bot_handler: Callable = lambda text: None
    ):
        self.__apikey = apikey
        self.__host = host
        self.__port = port
        self.__protocol = protocol
        self.__bot_handler = bot_handler
        self.__logger = logging.getLogger(__name__)

    async def start(self):
        self.__logger.info("started")
        session = aiohttp.ClientSession()
        async with session.ws_connect(f'{self.__protocol}://{self.__host}:{self.__port}/{self.__apikey}') as ws:
            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    try:
                        self.__logger.debug("new event received : " + msg.data)
                        tock_message: TockMessage = TockMessageSchema().load(json.loads(msg.data))
                        tock_response = self.__bot_handler(tock_message)
                        self.__logger.debug("new event sent : " + tock_response)
                        await ws.send_str(tock_response)
                    except JSONDecodeError:
                        e = sys.exc_info()[0]
                        self.__logger.exception(e)
                        pass
                elif msg.type == aiohttp.WSMsgType.CLOSED:
                    self.__logger.info("stopped")
                    break
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    self.__logger.error(msg.data)
                    break
