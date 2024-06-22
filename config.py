import os
from dotenv import load_dotenv


load_dotenv()

class Config():
    DEBUG = True
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DB_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'connect_args': {
            'connect_timeout': 20
        },
        'pool_recycle': 1800,
        'pool_pre_ping': True,
    }