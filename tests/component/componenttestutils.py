import logging
import unittest
import warnings


class BaseComponentTestCase(unittest.TestCase):
    SQS_LOCALSTACK = 'http://localhost:4566'
    REDIS_LOCALSTACK = 'localhost'

    @classmethod
    def setUpClass(cls):
        pass

    """
    Classe base para testes de componentes
    """

    def setUp(self):
        log_name = 'component_test'
        log_filename = None
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        logging.basicConfig(format=log_format, filename=log_filename, level=logging.DEBUG)
        self.logger = logging.getLogger(log_name)

        # ignora falso positivos
        # https://github.com/boto/boto3/issues/454
        warnings.filterwarnings("ignore", category=ResourceWarning, message="unclosed.*<ssl.SSLSocket.*>")
