# -*- coding: utf-8 -*-
import logging
import sys
from json import JSONDecodeError
from typing import Callable

import aiohttp

from tock.models import TockMessage, ClientConfiguration
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
            client_configuration: ClientConfiguration = None,
            bot_handler: Callable = lambda text: None
    ):
        self.__apikey = apikey
        self.__host = host
        self.__port = port
        self.__protocol = protocol
        self.__client_configuration = client_configuration
        self.__bot_handler = bot_handler
        self.__logger = logging.getLogger(__name__)

    async def start(self):
        self.__logger.info("started")
        session = aiohttp.ClientSession()
        async with session.ws_connect(f'{self.__protocol}://{self.__host}:{self.__port}/{self.__apikey}') as ws:
            await self.__send_bot_configuration(self.__client_configuration, ws)
            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    try:
                        self.__logger.debug(f"new event received {msg.data}")
                        tock_message_schema = TockMessageSchema()
                        tock_request: TockMessage = tock_message_schema.loads(msg.data)
                        tock_response = tock_message_schema.dumps(self.__bot_handler(tock_request))
                        self.__logger.debug(f"new event sent : {tock_response}")
                        await ws.send_str(tock_response)
                    except Exception as e:
                        self.__logger.exception(e)
                        pass
                elif msg.type == aiohttp.WSMsgType.CLOSED:
                    self.__logger.info("stopped")
                    break
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    self.__logger.error(msg.data)
                    break

    async def __send_bot_configuration(self, client_configuration, ws):
        tock_message_schema = TockMessageSchema()
        tock_message = TockMessage(bot_configuration=client_configuration)
        bot_configuration: str = tock_message_schema.dumps(tock_message)
        self.__logger.debug(f"bot configuration sent {bot_configuration}")
        await ws.send_str(bot_configuration)
