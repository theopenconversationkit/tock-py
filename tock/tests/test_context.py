# -*- coding: utf-8 -*-
import json
import unittest

from testfixtures import compare

from tock.bus import TockBotBus
from tock.context import Contexts, Context, MemoryContexts, ContextSchema
from tock.intent import Intent
from tock.story import story
from tock.tests.test_schemas import given_user_id, given_entity


def hello():
    pass


class TestContexts(unittest.TestCase):
    def test_getcontext_existing(self):
        user_id = given_user_id("id1")
        expected = Context(user_id)

        contexts = MemoryContexts()
        contexts.save(expected)

        result = contexts.getcontext(user_id)

        compare(expected, result)

    def test_getcontext_not_existing(self):
        user_id = given_user_id("id1")
        expected = Context(user_id)

        contexts = MemoryContexts()

        result = contexts.getcontext(user_id)

        compare(expected, result)

    def test_two_context(self):
        user_id = given_user_id("id1")
        user_id2 = given_user_id("id2")

        expected = Context(user_id)
        expected2 = Context(user_id2)

        contexts = MemoryContexts()

        contexts.save(expected)
        contexts.save(expected2)

        result = contexts.getcontext(user_id)
        result2 = contexts.getcontext(user_id2)

        compare(expected, result)
        compare(expected2, result2)

    def test_serialization(self):

        @story(
            intent="greetings",
            other_starter_intents=[],
            secondary_intents=[]
        )
        def hello(bus: TockBotBus):
            bus.send("Hello i'm a tock-py bot")

        user_id = given_user_id("id2")
        expected = Context(user_id)
        expected.previous_intent = Intent(name="greetings")
        hello_story = hello()
        expected.current_story = hello_story
        expected.add_entities([given_entity()])
        schema = ContextSchema()
        dumps = schema.dumps(expected)
        print(dumps)
        loads = json.loads(dumps)
        result: Context = schema.load(loads)
        result.current_story = hello_story
        compare(expected, result)

if __name__ == '__main__':
    unittest.main()