from pymongo import MongoClient
from config import config

client = MongoClient(config.DATABASE.MONGODB_CONNECTION_STRING)

def querystatus(insert_dict):
    status_table = client[config.DATABASE.MONGODB_DATABASE_NAME][config.TABLE.STATUS_TABLE]
    query = status_table.find_one(insert_dict)
    return query if query else None