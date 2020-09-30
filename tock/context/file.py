# -*- coding: utf-8 -*-
import os
import pickle

from tock.context.context import Context
from tock.context.contexts import Contexts
from tock.models import UserId


class FileContexts(Contexts):
    def __init__(self, basepath: str = './'):
        self.__basepath = basepath

    def getcontext(self, user_id: UserId) -> Context:
        filename = self.__filename(user_id)
        if os.path.isfile(filename):
            with open(filename, 'rb') as f:
                context = pickle.load(f)
            return context
        else:
            return Context(user_id)

    def save(self, context: Context):
        if not os.path.exists(self.__basepath):
            os.makedirs(self.__basepath)
        user_file = self.__filename(context.user_id)
        with open(user_file, "wb") as f:
            pickle.dump(context, f)

    def __filename(self, user_id: UserId):
        return self.__basepath + '/' + user_id.id + '.pkl'
