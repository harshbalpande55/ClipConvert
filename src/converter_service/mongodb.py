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

def updatstatus(msg,update_dict):
    AA_user_table = client[config.DATABASE.MONGODB_DATABASE_NAME][config.TABLE.STATUS_TABLE]
    query = AA_user_table.find_one({"video_id": msg['video_id'],"email": msg['email']})
    if query:
        newvalues = { "$set": update_dict}
        AA_user_table.update_one(query, newvalues)
        return 'updated successfully'
    else:
        print('Record not found')
        return None
