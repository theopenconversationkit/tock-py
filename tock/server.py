# -*- coding: utf-8 -*-
import asyncio
import logging
from enum import Enum

from aiohttp import web

from tock.helpers import buildMessage
from tock.schemas import TockMessageSchema
from tock.websocket import TockWebsocket


class TockMode(Enum):
    WEBHOOK = 'webhook'
    WEBSOCKET = 'websocket'


class TockServer:
    """
    Tock Web Server
    """

    def __init__(self,
                 mode: TockMode = TockMode.WEBSOCKET,
                 apikey: str = 'apikey_is_undefined',
                 host: str = 'demo-bot.tock.ai',
                 port: int = 443,
                 protocol: str = 'wss',
                 path: str = 'webhook_key'
                 ):
        self.__apikey = apikey
        self.__host = host
        self.__port = port
        self.__protocol = protocol
        self.__path = path
        self.__logger = logging.getLogger(__name__)
        app = web.Application()

        if mode == TockMode.WEBSOCKET:
            app.on_startup.append(self.__startWebsocket)
        if mode == TockMode.WEBHOOK:
            app.add_routes([
                web.post(f'/{self.__path}/webhook', self.__handleWebhook)
            ])
        app.add_routes([
            web.get('/healthcheck', self.__handle)
        ])
        web.run_app(app=app, port=5000)

    async def __startWebsocket(self, app):
        self.__logger.info("__startWebsocket")
        app['tock_websocket'] = asyncio.create_task(self.__listenWebSocket(app))

    async def __cleanupWebsocket(self, app):
        self.__logger.info("__cleanupWebsocket")
        app['tock_websocket'].cancel()
        await app['tock_websocket']

    async def __listenWebSocket(self, app):
        self.__logger.info("__listenWebSocket")
        websocket = TockWebsocket(
            apikey=self.__apikey,
            host=self.__host,
            port=self.__port,
            protocol=self.__protocol
        )
        await websocket.start()

    async def __handle(self, request):
        name = request.match_info.get('name', "Anonymous")
        text = "Hello, " + name
        return web.Response(text=text)

    async def __handleWebhook(self, request):
        self.__logger.debug("new event received")
        payload = await request.json()
        tock_message = TockMessageSchema().load(payload)
        response = buildMessage(
            request_id=tock_message.request_id,
            text="Yo from python webhook !!!!"
        )
        tock_response = TockMessageSchema().dumps(response)
        self.__logger.debug("new event sent : " + tock_response)
        return web.Response(text=tock_response)
