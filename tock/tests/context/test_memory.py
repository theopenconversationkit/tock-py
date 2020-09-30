# -*- coding: utf-8 -*-
import unittest

from testfixtures import compare

from tock.context.context import Context
from tock.context.memory import MemoryContexts
from tock.tests.test_schemas import given_user_id


class TestMemoryContexts(unittest.TestCase):
    def test_existing_context(self):
        # given an existing
        user_id = given_user_id("id1")
        expected = Context(user_id)
        contexts = MemoryContexts()
        contexts.save(expected)

        # when load context
        result = contexts.getcontext(user_id)

        # then load existing context
        compare(expected, result)

    def test_new_context(self):
        # given a new context
        user_id = given_user_id("id1")
        expected = Context(user_id)
        contexts = MemoryContexts()

        # when load context
        result = contexts.getcontext(user_id)

        # then load new context
        compare(expected, result)

    def test_existing_contexts(self):
        # given existing contexts
        user_id = given_user_id("id1")
        user_id2 = given_user_id("id2")
        expected = Context(user_id)
        expected2 = Context(user_id2)
        contexts = MemoryContexts()
        contexts.save(expected)
        contexts.save(expected2)

        # when load context
        result = contexts.getcontext(user_id)
        result2 = contexts.getcontext(user_id2)

        # then load existing contexts
        compare(expected, result)
        compare(expected2, result2)


if __name__ == '__main__':
    unittest.main()
