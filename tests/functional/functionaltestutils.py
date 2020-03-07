import logging
import os
import unittest
from chalicelib.boot import init, register_vendor

init()
register_vendor()


class BaseFunctionalTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    """
    Classe base para testes funcionais
    """

    def setUp(self):
        self.environ = {
            'DB_HOST': os.environ['DB_HOST'],
            'DB_USER': os.environ['DB_USER'],
            'DB_PASSWORD': os.environ['DB_PASSWORD'],
            'DB': os.environ['DB']
        }

        log_name = 'functional_test'
        log_filename = None
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        logging.basicConfig(format=log_format, filename=log_filename, level=logging.INFO)
        self.logger = logging.getLogger(log_name)
