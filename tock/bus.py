# -*- coding: utf-8 -*-
import abc
from typing import Callable, List, Union

from tock.intent import Intent, Intent, IntentName
from tock.context import Context
from tock.models import BotMessage, BotRequest, Entity, Sentence


class BotBus(abc.ABC):

    @abc.abstractmethod
    def send(self, message: BotMessage):
        pass

    @property
    @abc.abstractmethod
    def context(self) -> Context:
        pass

    @property
    @abc.abstractmethod
    def intent(self) -> Intent:
        pass

    @property
    @abc.abstractmethod
    def request(self) -> BotRequest:
        pass

    @abc.abstractmethod
    def entity(self, entity_type: str) -> Entity:
        pass

    @abc.abstractmethod
    def is_intent(self, intents: List[Intent]) -> bool:
        pass


class TockBotBus(BotBus):

    def __init__(self,
                 context: Context,
                 send: Callable,
                 request: BotRequest
                 ):
        self.__context = context
        self.__send = send
        self.__request = request

    def send(self, message: Union[str, BotMessage]):
        if type(message) == str:
            message = Sentence.Builder(message).build()
        self.__send(message)

    @property
    def context(self):
        return self.__context

    @property
    def intent(self) -> Intent:
        return Intent(self.__request.intent)

    @property
    def request(self):
        return self.__request

    def entity(self, entity_type: str) -> Entity:
        return self.context.entity(entity_type)

    def is_intent(self, intents: Union[IntentName, Intent, List[IntentName], List[Intent]]) -> bool:
        if type(intents) == IntentName:
            intents = [Intent(intents)]
        elif type(intents) == Intent:
            intents = [intents]
        elif type(intents) == List[IntentName]:
            intents = map(Intent, intents)
        return self.intent in intents
