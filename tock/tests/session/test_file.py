# -*- coding: utf-8 -*-
import unittest
from unittest import mock

from testfixtures import compare

from tock.session.session import Session
from tock.session.file import FileStorage
from tock.tests.test_schemas import given_user_id


class TestFileStorage(unittest.TestCase):

    @mock.patch('os.path.exists', return_value=False)
    @mock.patch('os.makedirs')
    @mock.patch('tock.session.file.open', create=True)
    @mock.patch('pickle.dump')
    def test_given_base_path_not_exists_then_create_it_and_save_session(self,
                                                                        pickle_dump_mock,
                                                                        open_mock,
                                                                        makedirs_mock,
                                                                        path_exists_mock):
        # given
        user_id = given_user_id("id1")
        session = Session(user_id)
        bot_storage = FileStorage("/tmp/test-tock-sessions")

        # when
        bot_storage.save(session)

        # then
        assert makedirs_mock.called
        assert pickle_dump_mock.called

    @mock.patch('os.path.exists', return_value=True)
    @mock.patch('os.makedirs')
    @mock.patch('tock.session.file.open', create=True)
    @mock.patch('pickle.dump')
    def test_given_base_path_exists_then_save_session(self,
                                                      pickle_dump_mock,
                                                      open_mock,
                                                      makedirs_mock,
                                                      path_exists_mock):
        # given
        user_id = given_user_id("id1")
        session = Session(user_id)
        session_storage = FileStorage("/tmp/test-tock-sessions")

        # when
        session_storage.save(session)

        # then
        assert not makedirs_mock.called
        assert pickle_dump_mock.called

    @mock.patch('os.path.isfile', return_value=True)
    @mock.patch('tock.session.file.open', create=True)
    @mock.patch('pickle.load')
    def test_given_existing_session_then_load_it(self,
                                                 pickle_load_mock,
                                                 open_mock,
                                                 os_path_isfile_mock):
        user_id = given_user_id("id1")

        session_storage = FileStorage()
        session_storage.get_session(user_id)

        assert pickle_load_mock.called

    @mock.patch('os.path.isfile', return_value=False)
    @mock.patch('pickle.load')
    def test_given_not_existing_session_then_create_it(self,
                                                       pickle_load_mock,
                                                       os_path_isfile_mock):
        user_id = given_user_id("id1")
        expected = Session(user_id)

        session_storage = FileStorage()
        result = session_storage.get_session(user_id)

        assert not pickle_load_mock.called
        compare(result, expected)


if __name__ == '__main__':
    unittest.main()
