# -*- coding: utf-8 -*-
import os
import pickle

from tock.session.storage import Storage
from tock.session.session import Session
from tock.models import UserId


class FileStorage(Storage):
    def __init__(self, basepath: str = './'):
        self.__basepath = basepath

    def get_session(self, user_id: UserId) -> Session:
        filename = self.__filename(user_id)
        if os.path.isfile(filename):
            with open(filename, 'rb') as f:
                session = pickle.load(f)
            return session
        else:
            return Session(user_id)

    def save(self, session: Session):
        if not os.path.exists(self.__basepath):
            os.makedirs(self.__basepath)
        user_file = self.__filename(session.user_id)
        with open(user_file, "wb") as f:
            pickle.dump(session, f)

    def __filename(self, user_id: UserId):
        return self.__basepath + '/' + user_id.id + '.pkl'
