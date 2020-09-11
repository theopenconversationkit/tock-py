# -*- coding: utf-8 -*-
from marshmallow import Schema, fields, EXCLUDE, post_load
from marshmallow_enum import EnumField
from marshmallow_oneofschema import OneOfSchema

from tock.models import TockMessage, BotRequest, User, UserId, ConnectorType, Message, Entity, RequestContext, \
    BotResponse, ResponseContext, \
    Sentence, I18nText, Suggestion, PlayerType, Card, AttachmentType, Attachment, Action, Carousel


def camelcase(s):
    parts = iter(s.split("_"))
    return next(parts) + "".join(i.title() for i in parts)


class EntitySchema(Schema):
    type = fields.String(required=True)
    role = fields.String(required=True)
    content = fields.String(required=False, allow_none=True)
    value = fields.String(required=False, allow_none=True)
    evaluated = fields.Boolean(required=True)
    # subEntities = fields.List(fields.Nested(EntitySchema), required=True)
    new = fields.Boolean(required=True)

    @post_load
    def make_entity(self, data, **kwargs):
        return Entity(**data)

    class Meta:
        unknown = EXCLUDE


class MessageSchema(Schema):
    type = fields.String(required=True)
    text = fields.String(required=True)

    @post_load
    def make_message(self, data, **kwargs):
        return Message(**data)

    class Meta:
        unknown = EXCLUDE


class ConnectorTypeSchema(Schema):
    id = fields.String(required=True)
    user_interface_type = fields.String(required=True)

    @post_load
    def make_connector_type(self, data, **kwargs):
        return ConnectorType(**data)

    def on_bind_field(self, field_name, field_obj):
        field_obj.data_key = camelcase(field_obj.data_key or field_name)

    class Meta:
        unknown = EXCLUDE


class UserIdSchema(Schema):
    id = fields.String(required=True)
    type = EnumField(PlayerType, by_value=True)
    client_id = fields.String(required=True, allow_none=True)

    @post_load
    def make_user_id(self, data, **kwargs):
        return UserId(**data)

    def on_bind_field(self, field_name, field_obj):
        field_obj.data_key = camelcase(field_obj.data_key or field_name)

    class Meta:
        unknown = EXCLUDE


class UserSchema(Schema):
    timezone = fields.String(required=True)
    locale = fields.String(required=True)
    test = fields.Boolean(required=True)

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)

    class Meta:
        unknown = EXCLUDE


class RequestContextSchema(Schema):
    namespace = fields.String(required=True)
    language = fields.String(required=True)
    connector_type = fields.Nested(ConnectorTypeSchema)
    user_interface = fields.String(required=True)
    application_id = fields.String(required=True)
    user_id = fields.Nested(UserIdSchema)
    bot_id = fields.Nested(UserIdSchema)
    user = fields.Nested(UserSchema)

    def on_bind_field(self, field_name, field_obj):
        field_obj.data_key = camelcase(field_obj.data_key or field_name)

    @post_load
    def make_request_context(self, data, **kwargs):
        return RequestContext(**data)

    class Meta:
        unknown = EXCLUDE


class I18nTextSchema(Schema):
    text = fields.String(required=True)
    args = fields.List(fields.String, required=True)
    to_be_translated = fields.Boolean(required=True)
    length = fields.Integer(required=True)
    key = fields.String(required=False, allow_none=True)

    def on_bind_field(self, field_name, field_obj):
        field_obj.data_key = camelcase(field_obj.data_key or field_name)

    @post_load
    def make_i18n_text(self, data, **kwargs):
        return I18nText(**data)

    class Meta:
        unknown = EXCLUDE


class SuggestionSchema(Schema):
    title = fields.Nested(I18nTextSchema, required=True)

    @post_load
    def make_suggestion(self, data, **kwargs):
        return Suggestion(**data)

    class Meta:
        unknown = EXCLUDE


class AttachmentSchema(Schema):
    url = fields.String(required=True)
    type = EnumField(AttachmentType, by_value=True, required=False)

    def on_bind_field(self, field_name, field_obj):
        field_obj.data_key = camelcase(field_obj.data_key or field_name)

    @post_load
    def make_attachment(self, data, **kwargs):
        return Attachment(**data)

    class Meta:
        unknown = EXCLUDE


class ActionSchema(Schema):
    title = fields.Nested(I18nTextSchema)
    url = fields.String(required=False)

    @post_load
    def make_suggestion(self, data, **kwargs):
        return Action(**data)

    class Meta:
        unknown = EXCLUDE


class BotMessageSchema(Schema):
    delay = fields.Integer(required=False)

    class Meta:
        unknown = EXCLUDE


class SentenceSchema(BotMessageSchema):
    text = fields.Nested(I18nTextSchema)
    suggestions = fields.List(fields.Nested(SuggestionSchema), required=True)

    @post_load
    def make_sentence(self, data, **kwargs):
        return Sentence(**data)

    class Meta:
        unknown = EXCLUDE


class CardSchema(BotMessageSchema):
    title = fields.Nested(I18nTextSchema, required=False)
    sub_title = fields.Nested(I18nTextSchema, required=False)
    attachment = fields.Nested(AttachmentSchema, required=False)
    actions = fields.List(fields.Nested(ActionSchema), required=True)

    def on_bind_field(self, field_name, field_obj):
        field_obj.data_key = camelcase(field_obj.data_key or field_name)

    @post_load
    def make_card(self, data, **kwargs):
        return Card(**data)

    class Meta:
        unknown = EXCLUDE


class UberCardSchema(OneOfSchema):
    type_field = "type"
    type_schemas = {"card": CardSchema}

    def get_obj_type(self, obj):
        if isinstance(obj, Card):
            return "card"
        else:
            raise Exception("Unknown object type: {}".format(obj.__class__.__name__))


class CarouselSchema(BotMessageSchema):
    cards = fields.List(fields.Nested(UberCardSchema), required=True)

    @post_load
    def make_carousel(self, data, **kwargs):
        return Carousel(**data)

    class Meta:
        unknown = EXCLUDE


class UberBotMessageSchema(OneOfSchema):
    type_field = "type"
    type_schemas = {"sentence": SentenceSchema, "card": CardSchema, "carousel": CarouselSchema}

    def get_obj_type(self, obj):
        if isinstance(obj, Sentence):
            return "sentence"
        elif isinstance(obj, Card):
            return "card"
        elif isinstance(obj, Carousel):
            return "carousel"
        else:
            raise Exception("Unknown object type: {}".format(obj.__class__.__name__))


class ResponseContextSchema(Schema):
    request_id = fields.String(required=True)
    date = fields.DateTime(required=True)

    def on_bind_field(self, field_name, field_obj):
        field_obj.data_key = camelcase(field_obj.data_key or field_name)

    @post_load
    def make_response_context(self, data, **kwargs):
        return ResponseContext(**data)

    class Meta:
        unknown = EXCLUDE
        datetimeformat = '%Y-%m-%dT%H:%M:%SZ'


class BotRequestSchema(Schema):
    intent = fields.String(required=True)
    entities = fields.List(fields.Nested(EntitySchema), required=True)
    message = fields.Nested(MessageSchema())
    story_id = fields.String(required=True)
    request_context = fields.Nested(RequestContextSchema, required=False)

    def on_bind_field(self, field_name, field_obj):
        field_obj.data_key = camelcase(field_obj.data_key or field_name)

    @post_load
    def make_bot_request(self, data, **kwargs):
        return BotRequest(**data)

    class Meta:
        unknown = EXCLUDE


class BotResponseSchema(Schema):
    messages = fields.List(fields.Nested(UberBotMessageSchema), required=True)
    story_id = fields.String(required=True)
    step = fields.String(required=False, allow_none=True)
    entities = fields.List(fields.Nested(EntitySchema), required=True)
    context = fields.Nested(ResponseContextSchema, required=True)

    def on_bind_field(self, field_name, field_obj):
        field_obj.data_key = camelcase(field_obj.data_key or field_name)

    @post_load
    def make_bot_response(self, data, **kwargs):
        return BotResponse(**data)

    class Meta:
        unknown = EXCLUDE


class TockMessageSchema(Schema):
    bot_request = fields.Nested(BotRequestSchema, required=False)
    bot_response = fields.Nested(BotResponseSchema, required=False)
    request_id = fields.String(required=True)

    def on_bind_field(self, field_name, field_obj):
        field_obj.data_key = camelcase(field_obj.data_key or field_name)

    @post_load
    def make_tockmessage(self, data, **kwargs):
        return TockMessage(**data)


class UnsupportedSchema:
    pass
