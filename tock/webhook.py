# -*- coding: utf-8 -*-
import logging
from typing import Callable

from aiohttp import web

from tock.schemas import TockMessageSchema


class TockWebhook:
    """
    Tock Webhook mode
    """

    def __init__(self,
                 host: str = '127.0.0.1',
                 port: int = 5000,
                 path: str = 'webhook_key',
                 bot_handler: Callable = lambda text: None
                 ):
        self.__host = host
        self.__port = port
        self.__path = path
        self.__bot_handler = bot_handler
        self.__logger = logging.getLogger(__name__)
        self.__app = web.Application()
        self.__app.add_routes([
            web.post(f'/{self.__path}/webhook', self.__webhook)
        ])

    def start(self):
        web.run_app(host=self.__host, app=self.__app, port=self.__port)

    async def __webhook(self, request):
        self.__logger.debug("new event received")
        bot_request = await request.json()
        tock_response = self.__bot_handler(TockMessageSchema().load(bot_request))

        self.__logger.debug("new event sent : " + tock_response)
        return web.Response(text=tock_response)
