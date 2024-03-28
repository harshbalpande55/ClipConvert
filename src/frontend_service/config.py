from decouple import config

class config:
    class ENVIRONMENT:
        ENV = config("ENV")
    
    class SECRET:
        APP_SECRET_KEY = config("APP_SECRET_KEY")
        APP_JWT_SECRET_KEY = config("APP_JWT_SECRET_KEY")
        APP_AES_KEY = config("APP_AES_KEY")
        LOGIN_BASE_URL = config("LOGIN_BASE_URL")
        GATEWAY_BASE_URL = config("GATEWAY_BASE_URL")
        
    class DATABASE:
        MONGODB_CONNECTION_STRING = config("MONGODB_CONNECTION_STRING")
        MONGODB_DATABASE_NAME = config("MONGODB_DATABASE_NAME")
        
    class TABLE:
        USER_TABLE = config('USER_TABLE')
        VIDEO_TABLE = config('VIDEO_TABLE')
        AUDIO_TABLE = config('AUDIO_TABLE')
        STATUS_TABLE = config('STATUS_TABLE')
