# -*- coding: utf-8 -*-
from datetime import datetime
from enum import Enum


class PlayerType(Enum):
    USER = 'user'
    BOT = 'bot'


class Entity:

    def __init__(self, type: str, role: str, evaluated: bool, new: bool, content: str = None, value: str = None, ):
        self.type = type
        self.role = role
        self.content = content
        self.value = value
        self.evaluated = evaluated
        self.subEntities = []
        self.new = new


class Message:

    def __init__(self, type: str, text: str):
        self.type = type
        self.text = text


class ConnectorType:

    def __init__(self, id: str, userInterfaceType: str):
        self.id = id
        self.user_interface_type = userInterfaceType


class UserId:

    def __init__(self, id: str, type: PlayerType, clientId: str = None):
        self.id = id
        self.type = type
        self.client_id = clientId


class User:

    def __init__(self, timezone: str, locale: str, test: bool):
        self.timezone = timezone
        self.locale = locale
        self.test = test


class RequestContext:

    def __init__(self, namespace: str, language: str, connectorType: ConnectorType, userInterface: str, applicationId: str, userId: UserId,
                 botId: UserId, user: User):
        self.namespace = namespace
        self.language = language
        self.connector_type = connectorType
        self.user_interface = userInterface
        self.application_id = applicationId
        self.user_id = userId
        self.bot_id = botId
        self.user = user


class Suggestion:

    def __init__(self, title: str):
        self.title = title


class I18nText:

    def __init__(self, text: str, args: [], toBeTranslated: bool, length: int, key: str = None):
        self.text = text
        self.args = args
        self.to_be_translated = toBeTranslated
        self.length = length
        self.key = key


class BotMessageSentence:

    def __init__(self, text: str, suggestions: [], delay: int):
        self.text = text
        self.suggestions = suggestions
        self.delay = delay
        self.type = 'sentence'


class ResponseContext:

    def __init__(self, requestId: str, date: datetime):
        self.request_id = requestId
        self.date = date


class BotRequest:

    def __init__(self, intent: str, entities: [], message: Message, storyId: str, context: RequestContext):
        self.intent = intent
        self.entities = entities
        self.message = message
        self.story_id = storyId
        self.context = context


class BotResponse:

    def __init__(self, messages, storyId: str, entities: [], context: ResponseContext, step: str = None):
        self.messages = messages
        self.story_id = storyId
        self.step = step
        self.entities = entities
        self.context = context


class TockMessage:

    def __init__(self, requestId: str, botRequest: BotRequest = None, botResponse: BotResponse = None):
        self.bot_request = botRequest
        self.bot_response = botResponse
        self.request_id = requestId
