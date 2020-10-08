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
        self.__stories: List[Type[Story]] = []

    def find_story(self, story_name: str) -> Optional[Type[Story]]:
        for _story in self.__stories:
            if _story.configuration().name == story_name:
                return _story

    def register_story(self, story_type: Type[Story]):

        self.__stories.append(story_type)

    def client_configuration(self) -> ClientConfiguration:
        configurations: List[StoryConfiguration] = []
        for _story in self.__stories:
            configurations.append(_story.configuration())
        return ClientConfiguration(configurations)
