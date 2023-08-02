import pymongo
from pymongo import MongoClient
from ApsSensorFault.constant.database import DATABASE_NAME
import certifi
ca = certifi.where()

# class MongoDBClient:
#     def __init__(self, database_name=DATABASE_NAME):
#         try:
#             if MongoDBClient.client is None:
#                 mongo_db_url = "mongodb://localhost:27017/"
#                 MongoDBClient.client = MongoClient(mongo_db_url, tlsCAFile=ca)
            
#             self.client = MongoDBClient.client
#             self.database = self.client[database_name]
#             self.database_name = database_name
        
#         except Exception as e:
#             raise e

class MongoDBClient:
    client = None
    def __init__(self, database_name=DATABASE_NAME) -> None:
        try:
            if MongoDBClient.client is None:
                mongo_db_url = "mongodb://localhost:27017/"
                MongoDBClient.client = pymongo.MongoClient(mongo_db_url)
            self.client = MongoDBClient.client
            self.database = self.client[database_name]
            self.database_name = database_name
        except Exception as e:
            raise e