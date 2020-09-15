# -*- coding: utf-8 -*-
import unittest
from unittest import TestCase

from tock.models import UserId, PlayerType


class TestUserId(TestCase):
    def test_equality(self):
        expected = UserId(
            id="id",
            type=PlayerType.BOT,
            client_id="client_id"
        )
        result = UserId(
            id="id",
            type=PlayerType.BOT,
            client_id="client_id"
        )

        assert expected == result


if __name__ == '__main__':
    unittest.main()
