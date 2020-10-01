# -*- coding: utf-8 -*-
import abc
from typing import Optional, Dict, Type, List

from tock.bus import BotBus, TockBotBus
from tock.intent import Intent
from tock.models import BotRequest, ClientConfiguration, StoryConfiguration, IntentName


class Story(abc.ABC):

    def __init__(self, request: BotRequest):
        self._request: BotRequest = request

    @classmethod
    def configuration(cls) -> StoryConfiguration:
        return StoryConfiguration(
            main_intent=cls.intent().name,
            name=cls.intent().name,
            other_starter_intents=list(map(lambda intent: intent.name, cls.other_starter_intents())),
            secondary_intents=list(map(lambda intent: intent.name, cls.secondary_intents())),
            steps=[]
        )

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
        return self.intent() == _intent or \
               _intent in self.other_starter_intents() or \
               _intent in self.secondary_intents()

    @abc.abstractmethod
    def answer(self, bus: BotBus):
        pass


def story(intent: IntentName, other_starter_intents: List[IntentName] = None,
          secondary_intents: List[IntentName] = None):
    if secondary_intents is None:
        secondary_intents = []
    if other_starter_intents is None:
        other_starter_intents = []

    def decorator(answer):
        def provide_story_type():
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

        return provide_story_type

    return decorator


@story(intent="unknown")
def unknown(bus: TockBotBus):
    bus.send("Default unknown handler")


class StoryDefinitions:

    def __init__(self):
        self.__story_configurations = []
        self.__definitions_by_main_intent: Dict[Intent, Type[Story]] = {}
        self.__definitions_by_other_starter_intents: Dict[Intent, List[Type[Story]]] = {}
        self.__definitions_by_secondary_intents: Dict[Intent, List[Type[Story]]] = {}

    def __find_story_by_name(self, story_name: str) -> Optional[Type[Story]]:
        for story in self.__definitions_by_main_intent.values():
            if story.configuration().name == story_name:
                return story

    def register_story(self, story_type: Type[Story]):

        self.__story_configurations.append(story_type.configuration())
        self.__definitions_by_main_intent[story_type.intent()] = story_type

        for intent in story_type.other_starter_intents():
            if intent not in self.__definitions_by_other_starter_intents:
                self.__definitions_by_other_starter_intents[intent] = []
            self.__definitions_by_other_starter_intents[intent].append(story_type)

        for intent in story_type.secondary_intents():
            if intent not in self.__definitions_by_secondary_intents:
                self.__definitions_by_secondary_intents[intent] = []
            self.__definitions_by_secondary_intents[intent].append(story_type)

    def find_story(self, intent: Intent, current_story_name: str) -> Optional[Type[Story]]:
        current_story: Optional[Type[Story]] = self.__find_story_by_name(current_story_name)
        if current_story and current_story.support(current_story, intent):
            return current_story

        if intent in self.__definitions_by_main_intent:
            return self.__definitions_by_main_intent[intent]

        if intent in self.__definitions_by_other_starter_intents and len(
                self.__definitions_by_other_starter_intents[intent]) > 0:
            return self.__definitions_by_other_starter_intents[intent][0]

    def client_configuration(self) -> ClientConfiguration:
        return ClientConfiguration(self.__story_configurations)
