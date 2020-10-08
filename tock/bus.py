# -*- coding: utf-8 -*-
import abc
import logging
from typing import Callable, List, Any

from tock.session.session import Session
from tock.intent import Intent
from tock.models import BotMessage, BotRequest, Entity, Sentence, IntentName


class BotBus(abc.ABC):

    @abc.abstractmethod
    def send(self, message: BotMessage):
        pass

    @property
    @abc.abstractmethod
    def session(self) -> Session:
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
                 session: Session,
                 send: Callable,
                 request: BotRequest
                 ):
        self.__logger: logging.Logger = logging.getLogger(__name__)
        self.__session = session
        self.__send = send
        self.__request = request

    def send(self, message: Any):
        if type(message) == str:
            message = Sentence.Builder(message).build()
        if issubclass(message.__class__, BotMessage):
            self.__send(message)
        else:
            self.__logger.error(f"Unable to send {message}. The type provided is not correct {type(message)}. "
                                "Only str and BotMessage are supported")

    @property
    def context(self):
        self.__logger.error("bus.context is deprecated since v0.0.1-dev8. You should use session()")
        return self.session

    @property
    def session(self):
        return self.__session

    @property
    def intent(self) -> Intent:
        return Intent(self.__request.intent)

    @property
    def request(self):
        return self.__request

    def entity(self, entity_type: str) -> Entity:
        return self.session.entity(entity_type)

    def is_intent(self, intents: Any) -> bool:
        if type(intents) == IntentName:
            intents = [Intent(intents)]
        elif type(intents) == Intent:
            intents = [intents]
        elif type(intents) == List[IntentName]:
            intents = map(Intent, intents)
        return self.intent in intents
