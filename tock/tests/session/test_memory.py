# -*- coding: utf-8 -*-
import unittest

from testfixtures import compare

from tock.session.session import Session
from tock.session.memory import MemoryStorage
from tock.tests.test_schemas import given_user_id


class TestMemoryStorage(unittest.TestCase):
    def test_existing_session(self):
        # given an existing
        user_id = given_user_id("id1")
        expected = Session(user_id)
        session_storage = MemoryStorage()
        session_storage.save(expected)

        # when load session
        result = session_storage.get_session(user_id)

        # then load existing session
        compare(expected, result)

    def test_new_session(self):
        # given a new session
        user_id = given_user_id("id1")
        expected = Session(user_id)
        session_storage = MemoryStorage()

        # when load session
        result = session_storage.get_session(user_id)

        # then load new session
        compare(expected, result)

    def test_existing_sessions(self):
        # given existing session
        user_id = given_user_id("id1")
        user_id2 = given_user_id("id2")
        expected = Session(user_id)
        expected2 = Session(user_id2)
        session_storage = MemoryStorage()
        session_storage.save(expected)
        session_storage.save(expected2)

        # when load session
        result = session_storage.get_session(user_id)
        result2 = session_storage.get_session(user_id2)

        # then load existing session_storage
        compare(expected, result)
        compare(expected2, result2)


if __name__ == '__main__':
    unittest.main()
