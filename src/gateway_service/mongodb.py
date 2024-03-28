from pymongo import MongoClient
import gridfs
from config import config

client = MongoClient(config.DATABASE.MONGODB_CONNECTION_STRING)
video_db = mp3_db = client[config.DATABASE.MONGODB_DATABASE_NAME]

# Initialize GridFS with the video_db
video_fs = gridfs.GridFS(video_db, collection=config.TABLE.VIDEO_TABLE)
mp3_fs = gridfs.GridFS(mp3_db, collection=config.TABLE.AUDIO_TABLE)

def insertstatus(insert_dict):
    status_table = client[config.DATABASE.MONGODB_DATABASE_NAME][config.TABLE.STATUS_TABLE]
    status_table.insert_one(insert_dict)

def querystatus(insert_dict):
    status_table = client[config.DATABASE.MONGODB_DATABASE_NAME][config.TABLE.STATUS_TABLE]
    query = status_table.find_one(insert_dict)
    return query if query else None

def getuserhistory(insert_dict):
    status_table = client[config.DATABASE.MONGODB_DATABASE_NAME][config.TABLE.STATUS_TABLE]
    query = status_table.find(insert_dict)
    return query if query else None
    