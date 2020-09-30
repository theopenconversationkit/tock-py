# -*- coding: utf-8 -*-
import json
import os
import pickle
import unittest
from unittest import mock

from testfixtures import compare

from tock.context import FileContexts, Context
from tock.tests.test_schemas import given_user_id


class TestFileContexts(unittest.TestCase):

    @mock.patch('tock.context.open', create=True)
    @mock.patch('json.dumps')
    def test_save(self, json_dump, open_mock):
        user_id = given_user_id("id1")
        context = Context(user_id)

        filecontext = FileContexts()
        filecontext.save(context)

        assert json.dumps.called

    @mock.patch('os.path.isfile', return_value=True)
    @mock.patch('tock.context.open', create=True)
    @mock.patch('json.loads')
    def test_getcontext_existing(self, json_load, open_mock, os_path_isfile_mock):
        user_id = given_user_id("id1")

        filecontext = FileContexts()
        filecontext.getcontext(user_id)

        assert json.loads.called

    @mock.patch('os.path.isfile', return_value=False)
    @mock.patch('json.loads')
    def test_getcontext_not_existing(self, json_loads, os_path_isfile_mock):
        user_id = given_user_id("id1")
        expected = Context(user_id)

        filecontext = FileContexts()
        result = filecontext.getcontext(user_id)

        assert not json.loads.called
        compare(result, expected)

if __name__ == '__main__':
    unittest.main()
