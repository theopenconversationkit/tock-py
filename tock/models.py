# -*- coding: utf-8 -*-
from __future__ import annotations
import abc
import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import List, Optional, Any

from isodate import parse_duration


class PlayerType(Enum):
    USER = "user"
    BOT = "bot"


IntentName = str


class Value(abc.ABC):
    pass


@dataclass
class AmountOfMoneyValue(Value):
    value: int
    unit: str


@dataclass
class Candidate:
    value: str
    probability: float


class DateGrain(Enum):
    TIMEZONE = "timezone"
    UNKNOWN = "unknown"
    SECOND = "second"
    MINUTE = "minute"
    HOUR = "hour"
    DAY_OF_WEEK = "day_of_week"
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    QUARTER = "quarter"
    YEAR = "year"


class DateValue(abc.ABC):
    pass


@dataclass
class DateEntityValue(DateValue):
    date: datetime
    grain: DateGrain


@dataclass
class DateIntervalEntityValue(DateValue):
    date: DateValue
    to_date: DateValue


@dataclass
class DistanceValue(Value):
    value: int
    unit: str


@dataclass
class DurationValue(Value):
    value: str

    def to_timedelta(self) -> timedelta:
        return parse_duration(self.value)


@dataclass
class EmailValue(Value):
    value: str


@dataclass
class NumberValue(Value):
    value: int


@dataclass
class OrdinalValue(Value):
    value: int


@dataclass
class PhoneNumberValue(Value):
    value: str


@dataclass
class StringValue(Value):
    value: str
    candidates: List[Candidate]


class TemperatureUnit(Enum):
    CELSIUS = "celsius"
    FAHRENHEIT = "fahrenheit"
    DEGREE = "degree"


@dataclass
class TemperatureValue(Value):
    value: int
    unit: TemperatureUnit


@dataclass
class UrlValue(Value):
    value: str


@dataclass
class VolumeValue(Value):
    value: int
    unit: str


@dataclass
class Entity:
    type: str
    role: str
    evaluated: bool
    sub_entities = []
    new: bool
    content: str = None
    value: Optional[Value] = None


@dataclass
class Message:
    type: str
    text: str


@dataclass
class ConnectorType:
    id: str
    user_interface_type: str


@dataclass
class UserId:
    id: str
    type: PlayerType
    client_id: Optional[str] = None


@dataclass
class User:
    timezone: str
    locale: str
    test: bool


@dataclass
class RequestContext:
    namespace: str
    language: str
    connector_type: ConnectorType
    user_interface: str
    application_id: str
    user_id: UserId
    bot_id: UserId
    user: User


@dataclass
class I18nText:
    text: str
    args: []
    to_be_translated: bool
    length: int
    key: Optional[str] = None


@dataclass
class Suggestion:
    title: I18nText


@dataclass
class BotMessage(abc.ABC):
    delay: int


@dataclass
class Sentence(BotMessage):
    text: I18nText
    suggestions: List[Suggestion]
    delay: int

    def __init__(self,
                 text: I18nText,
                 suggestions: List[Suggestion],
                 delay: int = 0):
        self.text = text
        self.suggestions = suggestions
        super().__init__(delay)

    class Builder:

        def __init__(self, text: str):
            self.__text = text
            self.__suggestions = []
            self.__delay = 0

        def with_text(self, text: Any):
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


@dataclass
class Attachment:
    url: str
    type: Optional[AttachmentType]


@dataclass
class Action:
    title: I18nText
    url: Optional[str]


@dataclass
class Card(BotMessage):
    title: Optional[I18nText]
    sub_title: Optional[I18nText]
    attachment: Optional[Attachment]
    actions: List[Action]
    delay: int

    def __init__(self,
                 title: Optional[I18nText],
                 sub_title: Optional[I18nText],
                 attachment: Optional[Attachment],
                 actions: List[Action],
                 delay: int = 0):
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

        def with_title(self, title: Any):
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

        def with_sub_title(self, sub_title: Any):
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

        def add_action(self, title: Any, url: Optional[str] = None):
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


@dataclass
class Carousel(BotMessage):
    cards: List[Card]
    delay: int

    def __init__(self, cards: List[Card], delay: int = 0):
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


@dataclass
class ResponseContext:
    request_id: str
    date: datetime


@dataclass
class BotRequest:
    intent: IntentName
    entities: List[Entity]
    message: Message
    story_id: str
    context: RequestContext = None


@dataclass
class BotResponse:
    messages: List[BotMessage]
    story_id: str
    step: Optional[str]
    context: ResponseContext
    entities: List[Entity]


@dataclass
class StepConfiguration:
    main_intent: IntentName
    name: str
    other_starter_intents: List[IntentName]
    secondary_intents: List[IntentName]


@dataclass
class StoryConfiguration:
    main_intent: IntentName
    name: str
    other_starter_intents: List[IntentName]
    secondary_intents: List[IntentName]
    steps: List[StepConfiguration]


@dataclass
class ClientConfiguration:
    stories: List[StoryConfiguration]


@dataclass
class TockMessage:
    request_id: str = uuid.uuid4()
    configuration: Optional[bool] = None
    bot_configuration: Optional[ClientConfiguration] = None
    bot_request: Optional[BotRequest] = None
    bot_response: Optional[BotResponse] = None
