# -*- coding: utf-8 -*-
"""
    The ``bot`` module
    ======================

    Use it to init a Tock BOT.

    :Example:

    >>> import os
    >>>> from tock.bot import TockBot
    >>> TockBot().namespace("my-bot").start_websocket(apikey=os.environ['TOCK_APIKEY'])

"""
import asyncio
import logging
from datetime import datetime
from typing import Callable, Type, List

from tock.bus import TockBotBus, BotBus
from tock.context import Context
from tock.intent import IntentName, Intent
from tock.models import TockMessage, BotRequest, BotMessage, BotResponse, ResponseContext
from tock.schemas import TockMessageSchema
from tock.story import Story, ErrorStory, Stories, story
from tock.webhook import TockWebhook
from tock.websocket import TockWebsocket


class TockBot:

    def __init__(self):
        self.__logger: logging.Logger = logging.getLogger(__name__)
        self.__namespace: str = "default"
        self.__bus = TockBotBus
        self.__stories = Stories()
        self.__error_handler: Callable = lambda send: send("Default error handler")
        self.__context = Context()

    def namespace(self, namespace: str):
        self.__namespace = namespace
        return self

    def register_bus(self, bus: BotBus):
        self.__bus = bus
        return self

    def error_handler(self, handler: Callable):
        self.__error_handler = handler
        return self

    def add_story(self, intent_name: IntentName, answer: Callable):
        story_class: Type[Story] = story(intent_name)(answer)()

        self.register_story(story_class)
        return self

    def register_story(self, story: Type[Story]):
        self.__stories.register_story(story)
        return self

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

    def __bot_handler(self, tock_message: TockMessage) -> str:
        messages: List[BotMessage] = []
        request: BotRequest = tock_message.bot_request

        story_class: Type[Story] = self.__stories.find_story(Intent(request.intent), self.__context.current_story)

        self.__context.entities = self.__context.entities + request.entities
        self.__context.current_story = story_class
        bus = self.__bus(
            context=self.__context,
            send=lambda bot_message: messages.append(bot_message),
            request=request
        )

        if story_class is not None:
            self.__logger.info("story found %s for intent %s", story_class.__name__, request.intent)
            story = self.__create(story_class, bus)
        else:
            self.__logger.info("No story for intent %s", request.intent)
            story = ErrorStory(request=request, answer=self.__error_handler)

        try:
            story.answer(bus)
        except:
            self.__logger.exception("Unexpected error")

        response = TockMessage(
            bot_response=BotResponse(
                messages=messages,
                story_id="story_id",
                step=None,
                context=ResponseContext(
                    request_id=tock_message.request_id,
                    date=datetime.now()
                ),
                entities=[]
            ),
            request_id=tock_message.request_id,
        )
        tock_response: str = TockMessageSchema().dumps(response)
        return tock_response

    def __create(self, story_class: Type[Story], bus: BotBus):
        story = story_class(request=bus.request)
        for entity in bus.context.entities:
            entity_type = entity.type.split(":")[1]
            if hasattr(story, entity_type):
                setattr(
                    story,
                    entity_type,
                    entity.content
                )
        return story
