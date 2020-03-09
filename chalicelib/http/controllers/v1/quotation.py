from chalicelib.enums.messages import MessagesEnum
from chalicelib.exceptions import ApiException
from chalicelib.http.request import ApiRequest
from chalicelib.http.response import ApiResponse
from chalicelib.services.v1.quotation import QuotationService


class QuotationController:

    def __init__(self, logger):
        """

        :param logger:
        """
        self.logger = logger
        self.service = QuotationService(logger)

    def list(self, app):
        """

                :param app:
                :return:
                """
        api_request = ApiRequest(app)
        api_response = ApiResponse(api_request)

        # if shipping_company_id:
        #     api_request.where['id_transportadora'] = shipping_company_id

        try:
            data = self.service.list(api_request)
            #total = self.service.count(api_request)
            total = 1
            api_response.set_data(data)
            api_response.set_total(total)

        except Exception as err:
            self.logger.error(err)
            if isinstance(err, ApiException):
                api_ex = err
            else:
                api_ex = ApiException(MessagesEnum.LIST_ERROR)
            api_response.set_exception(api_ex)

        return api_response.get_response()

