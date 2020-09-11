# -*- coding: utf-8 -*-
import abc


class Connector(abc.ABC):

    @abc.abstractmethod
    def send(self, message: str):
        pass


class BaseConnector(Connector):

    def send(self, message: str):
        print(message)
        pass
