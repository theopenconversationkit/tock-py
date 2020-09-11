# -*- coding: utf-8 -*-
import json
import unittest
from datetime import datetime
from unittest import TestCase

from testfixtures import compare

from tock.models import ConnectorType, Entity, Message, UserId, User, RequestContext, PlayerType, Suggestion, I18nText, \
    Sentence, \
    ResponseContext, BotRequest, BotResponse, TockMessage, Card, Attachment, AttachmentType, Action, Carousel
from tock.schemas import ConnectorTypeSchema, EntitySchema, MessageSchema, UserIdSchema, UserSchema, \
    RequestContextSchema, SuggestionSchema, \
    I18nTextSchema, ResponseContextSchema, BotRequestSchema, BotResponseSchema, TockMessageSchema, \
    CardSchema, SentenceSchema, AttachmentSchema, ActionSchema, CarouselSchema


def given_bot_request() -> BotRequest:
    return BotRequest(
        intent="intent",
        entities=[
            Entity(
                type="type",
                role="role",
                evaluated=True,
                new=False,
                content="content",
                value="value"
            )
        ],
        message=Message(
            type="type",
            text="text"
        ),
        story_id="story_id",
        request_context=RequestContext(
            namespace="namespace",
            language="fr",
            connector_type=ConnectorType(
                id="id",
                user_interface_type="text"
            ),
            user_interface="text",
            application_id="application_id",
            user_id=UserId(
                id="id",
                type=PlayerType.USER
            ),
            bot_id=UserId(
                id="id",
                type=PlayerType.BOT
            ),
            user=User(
                timezone="timezone",
                locale="fr_FR",
                test=False
            )
        )
    )


def given_bot_response() -> BotResponse:
    return BotResponse(
        messages=[
            given_sentence(),
            given_card(),
            given_carousel()
        ],
        story_id="story_id",
        entities=[],
        context=ResponseContext(
            request_id="request_id",
            date=datetime(2020, 1, 1, 0, 0, 0)
        ),
        step="step"
    )


def given_i18n_text(text: str = "text") -> I18nText:
    return I18nText(
        text=text,
        args=["one", "two", "three"],
        to_be_translated=True,
        length=4,
        key="key"
    )


def given_sentence() -> Sentence:
    return Sentence(
        text=given_i18n_text(),
        suggestions=[
            given_suggestion("action1"),
            given_suggestion("action2")
        ],
        delay=0
    )


def given_attachment() -> Attachment:
    return Attachment(
        url="http://image.svg",
        type=AttachmentType.IMAGE
    )


def given_action() -> Action:
    return Action(
        title=given_i18n_text("action"),
        url="http://action.com"
    )


def given_card() -> Card:
    return Card.Builder() \
        .with_title(given_i18n_text()) \
        .with_sub_title(given_i18n_text()) \
        .with_attachment("http://image.svg", AttachmentType.IMAGE) \
        .add_action(given_i18n_text("action"), "http://action.com") \
        .with_delay(0) \
        .build()


def given_carousel() -> Carousel:
    return Carousel.Builder() \
        .add_card(given_card()) \
        .add_card(given_card()) \
        .add_card(given_card()) \
        .build()


def given_user_id() -> UserId:
    return UserId(
        id="id",
        type=PlayerType.USER,
        client_id="client_id"
    )


def given_entity() -> Entity:
    return Entity(
        type="type",
        role="role",
        evaluated=True,
        new=False,
        content="content",
        value="value"
    )


def given_user() -> User:
    return User(
        timezone="timezone",
        locale="fr_FR",
        test=False
    )


def given_response_context() -> ResponseContext:
    return ResponseContext(
        request_id="request_id",
        date=datetime(2020, 1, 1, 0, 0, 0)
    )


def given_suggestion(title: str = "action") -> Suggestion:
    return Suggestion(
        title=given_i18n_text(title)
    )


def given_message() -> Message:
    return Message(
        type="type",
        text="text"
    )


def given_connector_type() -> ConnectorType:
    return ConnectorType(
        id="id",
        user_interface_type="text"
    )


def given_request_context() -> RequestContext:
    return RequestContext(
        namespace="namespace",
        language="fr",
        connector_type=given_connector_type(),
        user_interface="text",
        application_id="application_id",
        user_id=given_user_id(),
        bot_id=given_user_id(),
        user=given_user()
    )


def given_tock_message() -> TockMessage:
    return TockMessage(
        request_id="request_id",
        bot_request=given_bot_request(),
        bot_response=given_bot_response()
    )


class TestEntitySchema(TestCase):
    def test_json_serialization(self):
        expected = given_entity()
        schema = EntitySchema()
        result = schema.load(json.loads(schema.dumps(expected)))
        compare(expected, result)


class TestMessageSchema(TestCase):
    def test_json_serialization(self):
        expected = given_message()
        schema = MessageSchema()
        result: Message = schema.load(json.loads(schema.dumps(expected)))
        compare(expected, result)


class TestConnectorTypeSchema(TestCase):
    def test_json_serialization(self):
        expected = given_connector_type()
        schema = ConnectorTypeSchema()
        result: ConnectorType = schema.load(json.loads(schema.dumps(expected)))
        compare(expected, result)


class TestUserIdSchema(TestCase):
    def test_json_serialization(self):
        expected = given_user_id()
        schema = UserIdSchema()
        result: UserId = schema.load(json.loads(schema.dumps(expected)))
        compare(expected, result)


class TestUserSchema(TestCase):
    def test_json_serialization(self):
        expected = given_user()
        schema = UserSchema()
        result: User = schema.load(json.loads(schema.dumps(expected)))
        compare(expected, result)


class TestRequestContextSchema(TestCase):
    def test_json_serialization(self):
        expected = given_request_context()
        schema = RequestContextSchema()
        result: RequestContext = schema.load(json.loads(schema.dumps(expected)))
        compare(expected, result)


class TestSuggestionSchema(TestCase):
    def test_json_serialization(self):
        expected = given_suggestion()
        schema = SuggestionSchema()
        result: Suggestion = schema.load(json.loads(schema.dumps(expected)))
        compare(expected, result)


class TestI18nTextSchema(TestCase):
    def test_json_serialization(self):
        expected = given_i18n_text()
        schema = I18nTextSchema()
        result: I18nText = schema.load(json.loads(schema.dumps(expected)))
        compare(expected, result)


class TestSentenceSchema(TestCase):
    def test_json_serialization(self):
        expected = given_sentence()
        schema = SentenceSchema()
        dumps = schema.dumps(expected)
        loads = json.loads(dumps)
        result: Sentence = schema.load(loads)
        compare(expected, result)


class TestAttachmentSchema(TestCase):
    def test_json_serialization(self):
        expected = given_attachment()
        schema = AttachmentSchema()
        dumps = schema.dumps(expected)
        loads = json.loads(dumps)
        result: Attachment = schema.load(loads)
        compare(expected, result)


class TestActionSchema(TestCase):
    def test_json_serialization(self):
        expected = given_action()
        schema = ActionSchema()
        result: Action = schema.load(json.loads(schema.dumps(expected)))
        compare(expected, result)


class TestCardSchema(TestCase):
    def test_json_serialization(self):
        expected = given_card()
        schema = CardSchema()
        dumps = schema.dumps(expected)
        loads = json.loads(dumps)
        result: Card = schema.load(loads)
        compare(expected, result)


class TestCarouselSchema(TestCase):
    def test_json_serialization(self):
        expected = given_carousel()
        schema = CarouselSchema()
        dumps = schema.dumps(expected)
        loads = json.loads(dumps)
        result: Carousel = schema.load(loads)
        compare(expected, result)


class TestResponseContextSchema(TestCase):
    def test_json_serialization(self):
        expected = given_response_context()
        schema = ResponseContextSchema()
        dumps = schema.dumps(expected)
        loads = json.loads(dumps)
        result: Sentence = schema.load(loads)
        compare(expected, result)


class TestBotRequestSchema(TestCase):
    def test_json_serialization(self):
        expected = given_bot_request()
        schema = BotRequestSchema()
        dumps = schema.dumps(expected)
        loads = json.loads(dumps)
        result: BotRequest = schema.load(loads)
        compare(expected, result)


class TestBotResponseSchema(TestCase):
    def test_json_serialization(self):
        expected = given_bot_response()
        schema = BotResponseSchema()
        dumps = schema.dumps(expected)
        loads = json.loads(dumps)
        result: BotResponse = schema.load(loads)
        compare(expected, result)


class TestTockMessageSchema(TestCase):
    def test_json_serialization(self):
        expected = given_tock_message()
        schema = TockMessageSchema()
        result: TockMessage = schema.load(json.loads(schema.dumps(expected)))
        compare(expected, result)


if __name__ == '__main__':
    unittest.main()
