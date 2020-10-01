# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod

from tock.context.context import Context
from tock.models import UserId


class BotStorage(ABC):

    @abstractmethod
    def getcontext(self, user_id: UserId):
        pass

    @abstractmethod
    def save(self, context: Context):
        pass
