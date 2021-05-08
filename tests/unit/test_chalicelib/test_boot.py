import os
import unittest
from chalicelib.boot import load_dot_env, reset, is_loaded, load_env
from tests.unit.testutils import BaseUnitTestCase, get_function_name
from unittest_data_provider import data_provider


def get_env():
    return (None, True), ('dev', True), ('development', True), ('integration', True), ('staging', True), (
    'production', True)


def get_load_dot_env():
    return (None, True), ('dev', True), ('development', True), ('integration', True), ('staging', False), (
    'production', False)


class BootTestCase(BaseUnitTestCase):

    @data_provider(get_env)
    def test_load_env(self, env, expected):
        self.logger.info('Running test: %s - %s', get_function_name(__name__), env)
        reset()
        load_env(env)
        APP_TYPE = os.environ['APP_TYPE']
        if APP_TYPE == 'Chalice':
            self.assertEqual(is_loaded(), expected)
        else:
            self.skipTest('test_load_env - Ignored because the APP_TYPE {}'.format(APP_TYPE))

    @data_provider(get_load_dot_env)
    def test_load_dot_env(self, env, expected):
        self.logger.info('Running test: %s - %s', get_function_name(__name__), env)
        APP_TYPE = os.environ['APP_TYPE']
        if APP_TYPE == 'Flask':
            reset()
            load_dot_env(env)
            self.assertEqual(is_loaded(), expected)
        else:
            self.skipTest('test_load_dot_env - Ignored because the APP_TYPE {}'.format(APP_TYPE))


if __name__ == '__main__':
    unittest.main()
