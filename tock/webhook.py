# -*- coding: utf-8 -*-
import logging
from typing import Callable

from aiohttp import web

from tock.models import TockMessage, ClientConfiguration
from tock.schemas import TockMessageSchema


class TockWebhook:
    """
    Tock Webhook mode
    """

    def __init__(self,
                 host: str = '127.0.0.1',
                 port: int = 5000,
                 path: str = 'webhook_key',
                 client_configuration: ClientConfiguration = None,
                 bot_handler: Callable = lambda text: None

                 ):
        self.__host = host
        self.__port = port
        self.__path = path
        self.__bot_handler = bot_handler
        self.__client_configuration = client_configuration
        self.__logger = logging.getLogger(__name__)
        self.__app = web.Application()
        self.__app.add_routes([
            web.post(f'/{self.__path}/webhook', self.__webhook)
        ])

    def start(self):
        web.run_app(host=self.__host, app=self.__app, port=self.__port)

    async def __webhook(self, request):
        payload = await request.json()
        self.__logger.debug(f"new event received : {payload}")

        tock_message_schema = TockMessageSchema()
        tock_request: TockMessage = tock_message_schema.load(payload)
        if tock_request.configuration:
            return self.__send_bot_configuration(self.__client_configuration)
        else:
            tock_response = tock_message_schema.dumps(self.__bot_handler(tock_request))

        self.__logger.debug(f"new event sent : {tock_response}")
        return web.Response(text=tock_response)

    def __send_bot_configuration(self, client_configuration):
        tock_message_schema = TockMessageSchema()
        tock_message = TockMessage(bot_configuration=client_configuration)
        bot_configuration: str = tock_message_schema.dumps(tock_message)
        self.__logger.debug(f"bot configuration sent {bot_configuration}")
        return web.Response(text=bot_configuration)
