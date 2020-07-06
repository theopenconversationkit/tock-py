# -*- coding: utf-8 -*-
from marshmallow import Schema, fields, EXCLUDE, post_load, validate

from tock.models import TockMessage, BotRequest, User, UserId, ConnectorType, Message, Entity, RequestContext, BotResponse, ResponseContext, \
    BotMessageSentence, I18nText, Suggestion


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
    userInterfaceType = fields.String(required=True)

    @post_load
    def make_connector_type(self, data, **kwargs):
        return ConnectorType(**data)

    class Meta:
        unknown = EXCLUDE


class UserIdSchema(Schema):
    id = fields.String(required=True)
    type = fields.String(required=True, validate=validate.OneOf(['bot', 'user']))
    clientId = fields.String(required=True, allow_none=True)

    @post_load
    def make_user_id(self, data, **kwargs):
        return UserId(**data)

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
    connectorType = fields.Nested(ConnectorTypeSchema())
    userInterface = fields.String(required=True)
    applicationId = fields.String(required=True)
    userId = fields.Nested(UserIdSchema())
    botId = fields.Nested(UserIdSchema())
    user = fields.Nested(UserSchema())

    @post_load
    def make_request_context(self, data, **kwargs):
        return RequestContext(**data)

    class Meta:
        unknown = EXCLUDE


class SuggestionSchema(Schema):
    title = fields.String(required=True)

    @post_load
    def make_suggestion(self, data, **kwargs):
        return Suggestion(**data)

    class Meta:
        unknown = EXCLUDE


class I18nTextSchema(Schema):
    text = fields.String(required=True)
    args = fields.List(fields.String, required=True)
    toBeTranslated = fields.Boolean(required=True)
    length = fields.Integer(required=True)
    key = fields.String(required=False, allow_none=True)

    @post_load
    def make_i18n_text(self, data, **kwargs):
        return I18nText(**data)

    class Meta:
        unknown = EXCLUDE


class BotMessageSchema(Schema):
    type = fields.Str(validate=validate.OneOf(['sentence']))
    text = fields.Nested(I18nTextSchema)
    suggestions = fields.List(fields.Nested(SuggestionSchema), required=True)
    delay = fields.Integer(required=False)

    @post_load
    def make_bot_message(self, data, **kwargs):
        if (data['type'] == 'sentence'):
            del data['type']
            return BotMessageSentence(**data)
        raise UnsupportedSchema

    class Meta:
        unknown = EXCLUDE


class ResponseContextSchema(Schema):
    requestId = fields.String(required=True)
    date = fields.DateTime(required=True)

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
    storyId = fields.String(required=True)
    context = fields.Nested(RequestContextSchema())

    @post_load
    def make_bot_request(self, data, **kwargs):
        return BotRequest(**data)

    class Meta:
        unknown = EXCLUDE


class BotResponseSchema(Schema):
    messages = fields.List(fields.Nested(BotMessageSchema), required=True)
    storyId = fields.String(required=True)
    step = fields.String(required=False, allow_none=True)
    entities = fields.List(fields.Nested(EntitySchema), required=True)
    context = fields.Nested(ResponseContextSchema, required=True)

    @post_load
    def make_bot_response(self, data, **kwargs):
        return BotResponse(**data)

    class Meta:
        unknown = EXCLUDE


class TockMessageSchema(Schema):
    botRequest = fields.Nested(BotRequestSchema(), required=False)
    botResponse = fields.Nested(BotResponseSchema(), required=False)
    requestId = fields.String(required=True)

    @post_load
    def make_tockmessage(self, data, **kwargs):
        return TockMessage(**data)


class UnsupportedSchema:
    pass
