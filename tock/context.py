# -*- coding: utf-8 -*-
import json
import os
import os.path
import pickle
from abc import ABC, abstractmethod
from re import split
from typing import List, Optional, Type

from marshmallow import Schema, fields, EXCLUDE, post_load

from tock.intent import Intent
from tock.models import Entity, UserId
from tock.schemas import EntitySchema, UserIdSchema


class Context:

    def __init__(self,
                 user_id: UserId,
                 current_story: Optional[Type] = None,
                 previous_intent: Optional[Intent] = None,
                 entities: List[Entity] = []):
        self.__current_story: Optional[Type] = current_story
        self.__previous_intent: Optional[Intent] = previous_intent
        self.__entities = entities
        self.__user_id: UserId = user_id

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
    def current_story(self, story: Type):
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

    def add_entities(self, entities: List[Entity]):
        self.__entities = self.__entities + entities

    @property
    def entities(self):
        return self.__entities

        # def __getstate__(self):
        state = self.__dict__.copy()
        del state["_Context__current_story"]
        return state

        # def __setstate__(self, state):
        self.__current_story = None


class Contexts(ABC):

    @abstractmethod
    def getcontext(self, user_id: UserId):
        pass

    @abstractmethod
    def save(self, context: Context):
        pass


class MemoryContexts(Contexts):
    def __init__(self):
        self.__contexts: List[Context] = []

    def getcontext(self, user_id: UserId) -> Context:
        for context in self.__contexts:
            if context.user_id == user_id:
                return context

        return Context(user_id)

    def save(self, context: Context):
        for item in self.__contexts:
            if item.user_id == context.user_id:
                self.__contexts.remove(item)
        self.__contexts.append(context)


class FileContexts(Contexts):
    def __init__(self, pathsave: str = './'):
        self.__pathsave = pathsave

    def getcontext(self, user_id: UserId) -> Context:

        filename = self.__filename(user_id)
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                schema = ContextSchema()
                file_content = f.read()
                json_content = json.loads(file_content)
                context: Context = schema.loads(json_content)
            return context
        else:
            return Context(user_id)

    def save(self, context: Context):
        user_file = self.__filename(context.user_id)
        with open(user_file, "w") as f:
            schema = ContextSchema()
            dumps = schema.dumps(context)
            f.write(dumps)
            f.close()

    def __filename(self, user_id: UserId):
        if not os.path.exists(self.__pathsave):
            os.makedirs(self.__pathsave)
        return self.__pathsave + '/' + user_id.id + '.json'


class IntentSchema(Schema):
    name = fields.String(required=True)

    @post_load
    def make_intent(self, data, **kwargs):
        return Intent(**data)

    class Meta:
        unknown = EXCLUDE


class ContextSchema(Schema):
    previous_intent = fields.Nested(IntentSchema, required=False)
    entities = fields.List(fields.Nested(EntitySchema), required=True)
    user_id = fields.Nested(UserIdSchema, required=True)

    @post_load
    def make_context(self, data, **kwargs):
        return Context(**data)

    class Meta:
        unknown = EXCLUDE
