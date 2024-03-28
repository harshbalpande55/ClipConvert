from pymongo import MongoClient
from config import config

client = MongoClient(config.DATABASE.MONGODB_CONNECTION_STRING)

def queryUserData(email,password):
    user_table = client[config.DATABASE.MONGODB_DATABASE_NAME][config.TABLE.USER_TABLE]
    query = user_table.find_one({"email":email,"password":password})
    return query if query else None