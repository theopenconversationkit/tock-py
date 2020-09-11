# -*- coding: utf-8 -*-
import abc
from typing import Callable, Optional, Dict, Type, List

from tock.bus import BotBus
from tock.intent import Intent, Intent
from tock.models import BotRequest


class Story(abc.ABC):

    def __init__(self, request: BotRequest):
        self._request: BotRequest = request

    @staticmethod
    @abc.abstractmethod
    def intent() -> Intent:
        pass

    @staticmethod
    @abc.abstractmethod
    def other_starter_intents() -> List[Intent]:
        pass

    @staticmethod
    @abc.abstractmethod
    def secondary_intents() -> List[Intent]:
        pass

    @staticmethod
    def support(self, _intent: Intent) -> bool:
        return self.intent() == _intent or _intent in self.other_starter_intents() or _intent in self.secondary_intents()

    @abc.abstractmethod
    def answer(self, bus: BotBus):
        pass


def story(intent: str, other_starter_intents=None, secondary_intents=None):
    if secondary_intents is None:
        secondary_intents = []
    if other_starter_intents is None:
        other_starter_intents = []

    def decorator(answer):
        def provide_story_class():
            return type(
                f"{intent.capitalize()}Story",
                (Story, object),
                {
                    "intent": lambda: Intent(intent),
                    "other_starter_intents": lambda: list(map(Intent, other_starter_intents)),
                    "secondary_intents": lambda: list(map(Intent, secondary_intents)),
                    "answer": lambda _, bus: answer(bus)
                }
            )

        return provide_story_class

    return decorator


# TODO beurk
class ErrorStory(Story):
    @staticmethod
    def other_starter_intents() -> List[Intent]:
        pass

    @staticmethod
    def secondary_intents() -> List[Intent]:
        pass

    intent: Intent = None

    def __init__(self, request: BotRequest, answer: Callable = lambda send: send("")):
        self.__answer = answer
        super().__init__(request)

    def answer(self, bus: BotBus):
        self.__answer(bus)


class Stories:

    def __init__(self):
        self.__stories_by_main_intent: Dict[Intent, Type[Story]] = {}
        self.__stories_by_other_starter_intents: Dict[Intent, List[Type[Story]]] = {}
        self.__stories_by_secondary_intents: Dict[Intent, List[Type[Story]]] = {}

    def register_story(self, story_class: Type[Story]):

        self.__stories_by_main_intent[story_class.intent()] = story_class

        for intent in story_class.other_starter_intents():
            if intent not in self.__stories_by_other_starter_intents:
                self.__stories_by_other_starter_intents[intent] = []
            self.__stories_by_other_starter_intents[intent].append(story_class)

        for intent in story_class.secondary_intents():
            if intent not in self.__stories_by_secondary_intents:
                self.__stories_by_secondary_intents[intent] = []
            self.__stories_by_secondary_intents[intent].append(story_class)

    def find_story(self, intent: Intent, current_story: Type[Story]) -> Optional[Type[Story]]:

        if current_story and current_story.support(current_story, intent):
            return current_story

        if intent in self.__stories_by_main_intent:
            return self.__stories_by_main_intent[intent]

        if intent in self.__stories_by_other_starter_intents and len(self.__stories_by_other_starter_intents[intent]) > 0:
            return self.__stories_by_other_starter_intents[intent][0]
