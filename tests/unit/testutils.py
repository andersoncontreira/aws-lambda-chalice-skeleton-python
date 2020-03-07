import random
import string
import traceback
import logging
import unittest
from chalicelib.boot import init, register_vendor

init()
register_vendor()


def random_string(string_length=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(string_length))


def get_function_name(class_name=""):
    fn_name = class_name + "::" + traceback.extract_stack(None, 2)[0][2]
    if not class_name:
        fn_name = traceback.extract_stack(None, 2)[0][2]
    return fn_name


class BaseUnitTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    """
    Classe base para testes funcionais
    """

    def setUp(self):
        log_name = 'unit_test'
        log_filename = None
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        logging.basicConfig(format=log_format, filename=log_filename, level=logging.INFO)
        self.logger = logging.getLogger(log_name)
