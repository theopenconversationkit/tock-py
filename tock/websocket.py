# -*- coding: utf-8 -*-
import json
import logging

import aiohttp
import sys

from tock.helpers import buildMessage
from tock.schemas import TockMessageSchema


class TockWebsocket:
    """
    Tock Web Socket mode
    """

    def __init__(
            self,
            apikey="apikey_is_undefined",
            host="demo-bot.tock.ai",
            port=443,
            protocol="wss"
    ):
        self.__apikey = apikey
        self.__host = host
        self.__port = port
        self.__protocol = protocol
        self.__logger = logging.getLogger(__name__)

    async def start(self):
        self.__logger.info("started")
        session = aiohttp.ClientSession()
        async with session.ws_connect(f'{self.__protocol}://{self.__host}:{self.__port}/{self.__apikey}') as ws:
            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    try:
                        self.__logger.debug("new event received : " + msg.data)
                        tock_message = self.__load(msg.data)
                        response = buildMessage(
                            request_id=tock_message.request_id,
                            text="Yo from python websocket !!!!"
                        )
                        tock_response = TockMessageSchema().dumps(response)
                        self.__logger.debug("new event sent : " + tock_response)
                        await ws.send_str(tock_response)
                    except:
                        e = sys.exc_info()[0]
                        self.__logger.exception(e)
                        pass
                elif msg.type == aiohttp.WSMsgType.CLOSED:
                    self.__logger.info("stopped")
                    break
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    self.__logger.error(msg.data)
                    break

    def __load(self, payload):
        try:
            data = json.loads(payload)
            return TockMessageSchema().load(data)
        except Exception as ex:
            self.__logger.error(f'Error when loading json\n\npayload: {payload}', exc_info=True)
