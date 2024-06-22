from flask import Flask
from flask_bcrypt import Bcrypt
from config import Config  
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager




app = Flask(__name__) 
app.config.from_object(Config)


bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login_page'
login_manager.login_message_category = 'info'




from shop.admin import form
from shop.admin import models
from shop.admin import routes

from shop.customer import routes
from shop.customer import form
from shop.customer import models
