# import json
# import os
# import boto3
#
# from os import path
#
# from tests import ROOT_DIR
#
# if __package__:
#     current_path = os.path.abspath(os.path.dirname(__file__)).replace('/' + str(__package__), '', 1)
# else:
#     current_path = os.path.abspath(os.path.dirname(__file__))
#
# if not current_path[-1] == '/':
#     current_path += '/'
#
#
# class ConnectionHelper:
#     @staticmethod
#     def get_dynamodb_local_connection():
#         connection = boto3.resource('dynamodb',
#                                     endpoint_url='http://0.0.0.0:9000',
#                                     region_name="sa-east-1"
#                                     )
#         return connection
#
#
# class DynamoDBHelper:
#
#     @staticmethod
#     def get_connection():
#         """
#         :return:
#         """
#         return ConnectionHelper.get_dynamodb_local_connection()
#
#     @staticmethod
#     def drop_table(connection, table_name):
#         result = True
#         try:
#             table = connection.Table(table_name)
#             table_exists = table.table_status
#             if table_exists:
#                 table.delete()
#
#                 print(f"Deleting {table.name}...")
#                 table.wait_until_not_exists()
#             else:
#                 print(f"{table.name} not exists")
#         except Exception as err:
#             print(f"{table_name} not exists")
#
#         return result
#
#     @staticmethod
#     def sow_table(connection, table_name, file_name):
#         result = False
#         cnt = 0
#         try:
#             seeder_file = open(file_name, 'r')
#             seed_data = json.loads(seeder_file.read())
#             seeder_file.close()
#
#             table = connection.Table(table_name)
#
#             print(seed_data)
#             for item in seed_data:
#                 cnt += 1
#                 table.put_item(
#                     Item=item
#                 )
#         except Exception as ex:
#             result = False
#             print(ex)
#
#         print("Total of rows affected: %d" % cnt)
#         return result
#
#     @staticmethod
#     def create_table(connection, table_name, file_name):
#         result = False
#
#         table = connection.Table(table_name)
#         try:
#             table_exists = table.table_status
#         except Exception as err:
#             table_exists = False
#
#         if not table_exists:
#             sql_file = open(file_name, 'r')
#             create_table = json.loads(sql_file.read())
#             sql_file.close()
#
#             params = create_table
#             params['TableName'] = table_name
#             table = connection.create_table(**params)
#             print(f"Creating {table_name}...")
#             table.wait_until_exists()
#             result = True
#         else:
#             print(f'Table {table_name} already exists')
#         return result
