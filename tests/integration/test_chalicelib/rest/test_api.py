import unittest

from chalicelib.rest.api import Api
from tests.integration.integrationtestutils import BaseIntegrationTestCase
from tests.unit.testutils import get_function_name


class ApiTestCase(BaseIntegrationTestCase):

    def test_request(self):
        self.logger.info('Running test: %s', get_function_name(__name__))
        api = Api()
        url = '{}/{}'.format(self.config.API_URL, 657705)
        headers = api.build_headers_from_string(self.config.API_TOKEN)

        api.request(api.GET, url, headers=headers)
        response = api.exec()
        api.log(response)
        self.assertEqual(response.status_code, 200)

    def test_get(self):
        self.logger.info('Running test: %s', get_function_name(__name__))
        api = Api()
        url = '{}/{}'.format(self.config.API_URL, 657705)
        headers = api.build_headers_from_string(self.config.API_TOKEN)

        response = api.get(url, headers=headers)
        api.log(response)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
