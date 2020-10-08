# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod

from tock.session.session import Session
from tock.models import UserId


class Storage(ABC):

    @abstractmethod
    def get_session(self, user_id: UserId) -> Session:
        pass

    @abstractmethod
    def save(self, session: Session):
        pass
