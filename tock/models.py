# -*- coding: utf-8 -*-
import abc
from datetime import datetime
from enum import Enum
from re import split
from typing import List, Union, Optional

from tock.intent import IntentName


class PlayerType(Enum):
    USER = "user"
    BOT = "bot"


class Entity:

    def __init__(self, type: str, role: str, evaluated: bool, new: bool, content: str = None, value: str = None):
        self.type = type
        self.role = role
        self.content = content
        self.value = value
        self.evaluated = evaluated
        self.sub_entities = []
        self.new = new


class Message:

    def __init__(self, type: str, text: str):
        self.type = type
        self.text = text


class ConnectorType:

    def __init__(self, id: str, user_interface_type: str):
        self.id = id
        self.user_interface_type = user_interface_type


class UserId:

    def __init__(self, id: str, type: PlayerType, client_id: str = None):
        self.id = id
        self.type = type
        self.client_id = client_id


class User:

    def __init__(self, timezone: str, locale: str, test: bool):
        self.timezone = timezone
        self.locale = locale
        self.test = test


class RequestContext:

    def __init__(self,
                 namespace: str,
                 language: str,
                 connector_type: ConnectorType,
                 user_interface: str,
                 application_id: str,
                 user_id: UserId,
                 bot_id: UserId,
                 user: User):
        self.namespace = namespace
        self.language = language
        self.connector_type = connector_type
        self.user_interface = user_interface
        self.application_id = application_id
        self.user_id = user_id
        self.bot_id = bot_id
        self.user = user


class I18nText:

    def __init__(self,
                 text: str,
                 args: [],
                 to_be_translated: bool,
                 length: int,
                 key: Optional[str] = None
                 ):
        self.text = text
        self.args = args
        self.to_be_translated = to_be_translated
        self.length = length
        self.key = key


class Suggestion:

    def __init__(self, title: I18nText):
        self.title = title


class BotMessage(abc.ABC):

    def __init__(self, delay: int = 0):
        self.delay = delay


class Sentence(BotMessage):

    def __init__(self,
                 text: I18nText,
                 suggestions: List[Suggestion],
                 delay: int):
        self.text = text
        self.suggestions = suggestions
        super().__init__(delay)

    class Builder:

        def __init__(self, text: str):
            self.__text = text
            self.__suggestions = []
            self.__delay = 0

        def with_text(self, text: Union[str, I18nText]):
            if isinstance(text, I18nText):
                self.__text = text
            else:
                self.__text = I18nText(
                    text=text,
                    args=[],
                    to_be_translated=True,
                    length=len(text)
                )
            return self

        def add_suggestion(self, title: str):
            self.__suggestions.append(Suggestion(
                title=I18nText(
                    text=title,
                    args=[],
                    to_be_translated=True,
                    length=len(self.__text)
                )
            ))
            return self

        def with_delay(self, delay: int):
            self.__delay = delay
            return self

        def build(self):
            return Sentence(
                text=I18nText(
                    text=self.__text,
                    args=[],
                    to_be_translated=True,
                    length=len(self.__text)
                ),
                suggestions=self.__suggestions,
                delay=self.__delay
            )


class AttachmentType(Enum):
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"
    FILE = "file"


class Attachment:

    def __init__(self, url: str, type: Optional[AttachmentType]):
        self.url = url
        self.type = type


class Action:

    def __init__(self, title: I18nText, url: Optional[str]):
        self.title = title
        self.url = url


class Card(BotMessage):

    def __init__(self,
                 title: Optional[I18nText],
                 sub_title: Optional[I18nText],
                 attachment: Optional[Attachment],
                 actions: List[Action],
                 delay: int):
        self.title = title
        self.sub_title = sub_title
        self.attachment = attachment
        self.actions = actions
        super().__init__(delay)

    class Builder:

        def __init__(self):
            self.__title = None
            self.__sub_title = None
            self.__attachment = None
            self.__actions: List[Action] = []
            self.__delay = 0

        def with_title(self, title: Union[str, I18nText]):
            if isinstance(title, I18nText):
                self.__title = title
            else:
                self.__title = I18nText(
                    text=title,
                    args=[],
                    to_be_translated=True,
                    length=len(title)
                )
            return self

        def with_sub_title(self, sub_title: Union[str, I18nText]):
            if isinstance(sub_title, I18nText):
                self.__sub_title = sub_title
            else:
                self.__sub_title = I18nText(
                    text=sub_title,
                    args=[],
                    to_be_translated=True,
                    length=len(sub_title)
                )
            return self

        def with_attachment(self, url: str, type: AttachmentType = None):
            self.__attachment = Attachment(url, type)
            return self

        def add_action(self, title: Union[str, I18nText], url: str):
            if not isinstance(title, I18nText):
                title = I18nText(
                    text=title,
                    args=[],
                    to_be_translated=True,
                    length=len(title)
                )
            self.__actions.append(Action(title=title, url=url))
            return self

        def with_delay(self, delay: int):
            self.__delay = delay
            return self

        def build(self):
            return Card(
                title=self.__title,
                sub_title=self.__sub_title,
                attachment=self.__attachment,
                actions=self.__actions,
                delay=self.__delay
            )


class Carousel(BotMessage):

    def __init__(self, cards: List[Card], delay: int):
        self.cards = cards
        super().__init__(delay)

    class Builder:

        def __init__(self):
            self.__cards: List[Card] = []
            self.__delay = 0

        def add_card(self, card: Card):
            self.__cards.append(card)
            return self

        def build(self):
            return Carousel(
                cards=self.__cards,
                delay=self.__delay
            )


class ResponseContext:

    def __init__(self, request_id: str, date: datetime):
        self.request_id = request_id
        self.date = date


class BotRequest:

    def __init__(self, intent: IntentName, entities: List[Entity], message: Message, story_id: str,
                 request_context: RequestContext = None):
        self.intent = intent
        self.entities = entities
        self.message = message
        self.story_id = story_id
        self.request_context = request_context


class BotResponse:

    def __init__(self, messages: List[BotMessage], story_id: str, step: str, context: ResponseContext,
                 entities: List[Entity]):
        self.messages = messages
        self.story_id = story_id
        self.step = step
        self.entities = entities
        self.context = context


class TockMessage:

    def __init__(self, request_id: str, bot_request: BotRequest = None, bot_response: BotResponse = None):
        self.bot_request = bot_request
        self.bot_response = bot_response
        self.request_id = request_id
