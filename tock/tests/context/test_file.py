# -*- coding: utf-8 -*-
import unittest
from unittest import mock

from testfixtures import compare

from tock.context.context import Context
from tock.context.file import FileContexts
from tock.tests.test_schemas import given_user_id


class TestFileContexts(unittest.TestCase):

    @mock.patch('os.path.exists', return_value=False)
    @mock.patch('os.makedirs')
    @mock.patch('tock.context.file.open', create=True)
    @mock.patch('pickle.dump')
    def test_given_base_path_not_exists_then_create_it_and_save_context(self,
                                                                        pickle_dump_mock,
                                                                        open_mock,
                                                                        makedirs_mock,
                                                                        path_exists_mock):
        # given
        user_id = given_user_id("id1")
        context = Context(user_id)
        file_contexts = FileContexts("/tmp/test-tock-contexts")

        # when
        file_contexts.save(context)

        # then
        assert makedirs_mock.called
        assert pickle_dump_mock.called

    @mock.patch('os.path.exists', return_value=True)
    @mock.patch('os.makedirs')
    @mock.patch('tock.context.file.open', create=True)
    @mock.patch('pickle.dump')
    def test_given_base_path_exists_then_save_context(self,
                                                      pickle_dump_mock,
                                                      open_mock,
                                                      makedirs_mock,
                                                      path_exists_mock):
        # given
        user_id = given_user_id("id1")
        context = Context(user_id)
        file_contexts = FileContexts("/tmp/test-tock-contexts")

        # when
        file_contexts.save(context)

        # then
        assert not makedirs_mock.called
        assert pickle_dump_mock.called

    @mock.patch('os.path.isfile', return_value=True)
    @mock.patch('tock.context.file.open', create=True)
    @mock.patch('pickle.load')
    def test_given_existing_context_then_load_it(self,
                                                 pickle_load_mock,
                                                 open_mock,
                                                 os_path_isfile_mock):
        user_id = given_user_id("id1")

        file_contexts = FileContexts()
        file_contexts.getcontext(user_id)

        assert pickle_load_mock.called

    @mock.patch('os.path.isfile', return_value=False)
    @mock.patch('pickle.load')
    def test_given_not_existing_context_then_create_it(self,
                                                       pickle_load_mock,
                                                       os_path_isfile_mock):
        user_id = given_user_id("id1")
        expected = Context(user_id)

        file_contexts = FileContexts()
        result = file_contexts.getcontext(user_id)

        assert not pickle_load_mock.called
        compare(result, expected)


if __name__ == '__main__':
    unittest.main()
