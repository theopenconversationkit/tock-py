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
import abc
import logging
from datetime import datetime
from typing import Callable, Type, List, Any

import asyncio

from tock.bus import TockBotBus, BotBus
from tock.session.storage import Storage
from tock.session.memory import MemoryStorage
from tock.intent import Intent
from tock.models import TockMessage, BotRequest, BotMessage, \
    BotResponse, ResponseContext, IntentName, ClientConfiguration, UserId
from tock.story import Story, StoryDefinitions, story as story_decorator, unknown
from tock.webhook import TockWebhook
from tock.websocket import TockWebsocket


class TockBot:

    def __init__(self):
        self.__logger: logging.Logger = logging.getLogger(__name__)
        self.__namespace: str = "default"
        self.__bus: Type[TockBotBus] = TockBotBus
        self.__story_definitions: StoryDefinitions = StoryDefinitions()
        self.__bot_storage: Storage = MemoryStorage()

    def __add_story(self, intent_name: IntentName, answer: Callable) -> 'TockBot':
        story_class: Type[Story] = story_decorator(intent_name)(answer)()
        self.register_story(story_class)
        return self

    def namespace(self, namespace: str) -> 'TockBot':
        self.__namespace = namespace
        return self

    def use_storage(self, storage: Storage) -> 'TockBot':
        self.__bot_storage = storage
        return self

    def register_bus(self, bus: Type[BotBus]) -> 'TockBot':
        self.__bus = bus
        return self

    def register_story(self, story: Any) -> 'TockBot':
        if type(story) == abc.ABCMeta:
            self.__story_definitions.register_story(story)
        elif story.__name__ == "provide_story_type":
            self.__story_definitions.register_story(story())
        else:
            self.__add_story(story.__name__, story)
        return self

    def register_stories(self, *stories: Any) -> 'TockBot':
        for story in stories:
            self.register_story(story)
        return self

    def client_configuration(self) -> ClientConfiguration:
        return self.__story_definitions.client_configuration()

    def start_webhook(self,
                      host: str,
                      path: str,
                      port: int):
        TockWebhook(
            host=host,
            path=path,
            port=port,
            client_configuration=self.client_configuration(),
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
            client_configuration=self.client_configuration(),
            bot_handler=self.__bot_handler
        ).start())

    def __bot_handler(self, tock_message: TockMessage) -> TockMessage:
        self.__logger.debug(f"receive tock_message {tock_message}")
        messages: List[BotMessage] = []
        request: BotRequest = tock_message.bot_request
        current_user_id: UserId = request.context.user_id

        session = self.__bot_storage.get_session(current_user_id)
        session.entities = request.entities

        story_type: Type[Story] = self.__story_definitions.find_story(request.story_id)
        session.previous_intent = Intent(request.intent)

        bus = self.__bus(
            session=session,
            send=lambda bot_message: messages.append(bot_message),
            request=request
        )

        if story_type is not None:
            story_name: str = story_type.configuration().name
            self.__logger.info("story found %s for intent %s", story_name, request.intent)
            session.current_story = story_name
        else:
            self.__logger.info("No story for intent %s", request.intent)
            story_type = unknown()

        story_instance: Story = self.__create(story_type, bus)

        try:
            story_instance.answer(bus)
        except:
            self.__logger.exception("Unexpected error")

        response = TockMessage(
            bot_response=BotResponse(
                messages=messages,
                story_id=story_instance.configuration().name,
                step=None,
                context=ResponseContext(
                    request_id=tock_message.request_id,
                    date=datetime.now()
                ),
                entities=request.entities
            ),
            request_id=tock_message.request_id,
        )
        self.__logger.debug(f"send tock_message {response}")
        self.__bot_storage.save(session)
        return response

    @staticmethod
    def __create(story_class: Type[Story], bus: BotBus):
        story = story_class(request=bus.request)
        for entity in bus.session.entities:
            entity_type = entity.type.split(":")[1]
            if hasattr(story, entity_type):
                setattr(
                    story,
                    entity_type,
                    entity.content
                )
        return story
