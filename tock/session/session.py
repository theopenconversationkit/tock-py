# -*- coding: utf-8 -*-
from re import split
from typing import Optional, List, Any

from tock.intent import Intent
from tock.models import Entity, UserId


class Session:

    def __init__(self,
                 user_id: UserId,
                 current_story: Optional[str] = None,
                 previous_intent: Optional[Intent] = None,
                 entities: List[Entity] = None):
        if entities is None:
            entities = []
        self.__current_story: Optional[str] = current_story
        self.__previous_intent: Optional[Intent] = previous_intent
        self.__entities = entities
        self.__user_id: UserId = user_id
        self.__items = {}

    def entity(self, entity_type: str) -> Optional[Entity]:
        for entity in reversed(self.entities):
            parts = split(':', entity.type)
            parts.reverse()
            if parts[0] == entity_type:
                return entity

    @property
    def current_story(self):
        return self.__current_story

    @current_story.setter
    def current_story(self, story: str):
        self.__current_story = story

    @property
    def previous_intent(self):
        return self.__previous_intent

    @previous_intent.setter
    def previous_intent(self, intent: Intent):
        self.__previous_intent = intent

    @property
    def user_id(self):
        return self.__user_id

    @property
    def entities(self):
        return self.__entities

    @entities.setter
    def entities(self, entities: List[Entity]):
        self.__entities = entities

    def reset_entities(self):
        self.__entities = []

    def add_entities(self, entities: List[Entity]):
        self.__entities = self.__entities + entities

    def set_item(self, key: str, value: Any):
        self.__items[key] = value

    def get_item(self, key: str) -> Optional[Any]:
        if key in self.__items.keys():
            return self.__items[key]

    def clear(self):
        self.__items = {}
