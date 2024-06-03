from flask import Flask
from config import Config


# initialize flask
app = Flask(__name__)
# configure app to debug mode
app.config.from_object(Config)

# configure with secret key 
app.config["SECRET_KEY"] = "FDGHUIOIUGFCSVJUGGH987TGHJ"

# import all routes modules
from shop.routes.root import *
from shop.routes.admin import *