# -*- coding: utf-8 -*-
from typing import List

from tock.session.storage import Storage
from tock.session.session import Session
from tock.models import UserId


class MemoryStorage(Storage):
    def __init__(self):
        self.__sessions: List[Session] = []

    def get_session(self, user_id: UserId) -> Session:
        for session in self.__sessions:
            if session.user_id == user_id:
                return session

        return Session(user_id)

    def save(self, session: Session):
        for item in self.__sessions:
            if item.user_id == session.user_id:
                self.__sessions.remove(item)
        self.__sessions.append(session)
