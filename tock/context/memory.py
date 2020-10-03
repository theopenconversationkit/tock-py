# -*- coding: utf-8 -*-
from typing import List

from tock.context.botstorage import BotStorage
from tock.context.context import Context
from tock.models import UserId


class MemoryStorage(BotStorage):
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
