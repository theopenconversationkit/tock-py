# -*- coding: utf-8 -*-
from typing import Callable

import asyncio

from tock.helpers import buildBotResponse, buildMessage
from tock.schemas import TockMessageSchema
from tock.webhook import TockWebhook
from tock.websocket import TockWebsocket


class TockBot:

    def __init__(self):
        self.__story_handlers = {}

    def add_story(self, intent: str, handler: Callable):
        self.__story_handlers[intent] = handler

    def start_webhook(self,
                      host: str,
                      path: str,
                      port: int):
        TockWebhook(
            host=host,
            path=path,
            port=port,
            bot_handler=self.__bot_handler
        ).start()

    def start_websocket(self,
                        apikey: str = 'apikey_is_undefined',
                        host: str = 'demo-bot.tock.ai',
                        port: int = 443,
                        protocol: str = 'wss'):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(TockWebsocket(
            apikey=apikey,
            host=host,
            port=port,
            protocol=protocol,
            bot_handler=self.__bot_handler
        ).start())

    def __bot_handler(self, bot_request):
        tock_message = TockMessageSchema().load(bot_request)
        messages = []
        self.__story_handlers[tock_message.bot_request.intent](
            lambda text: messages.append(buildMessage(text=text))
        )
        response = buildBotResponse(
            request_id=tock_message.request_id,
            messages=messages
        )
        tock_response = TockMessageSchema().dumps(response)
        return tock_response
