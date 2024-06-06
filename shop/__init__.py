from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os


# initialize flask
app = Flask(__name__)
app.config.from_object(Config)

load_dotenv()

# configure with secret key 
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

# configure with database
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DB_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# import all routes modules
from shop.routes.root import *
from shop.routes.admin import *

from shop.models.root import *
from shop.models.admin import *