# from chalicelib import database
#
#
# class AbstractService:
#     DEBUG = False
#     ENTITY = None
#     REPOSITORY = None
#     VALIDATOR = None
#
#     def __init__(self, logger=None):
#         self.VERSION = 'v1'
#         self.logger = logger
#         # habilitar se tiver conexão
#         # self.connection = database.get_connection()
#         self.connection = None
#         self._repository = None
#         self.validator = None
#
#         # habilitar se tiver repositorios
#         # if not self.REPOSITORY:
#         #     raise Exception('REPOSITORY must be defined')
#
#         # habilitar se tiver validadores
#         # if not self.VALIDATOR:
#         #     raise Exception('VALIDATOR must be defined')
#
#         # habilitar se tiver repositorios
#         # if self.DEBUG:
#         #     self._repository = self.REPOSITORY(self.connection, logger)
#         # else:
#         #     self._repository = self.REPOSITORY(self.connection)
#
#         # habilitar se tiver validadores
#         # if self.VALIDATOR:
#         #     self.validator = self.VALIDATOR(self.logger)
#
#     def validate_request(self, api_request):
#
#         if self.logger:
#             self.logger.info('Validating Request...')
#
#         if not database.check_connection(self.connection):
#             ex = Exception('Database not connected')
#             raise ex
#
#         # BUGFIX: copy() Vai evitar a sobrescrita de valores na requisição original
#         request = api_request.deepcopy(self.logger).to_dict()
#
#         if self.logger:
#             self.logger.info('validating request')
#
#         if not self.validator.validate(request):
#             raise self.validator.exception
#
#         if self.logger:
#             self.logger.info('Request: {}'.format(request))
#
#         return request
