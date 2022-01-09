from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("Flask_Secret_1")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "danger"

# from selfwebapp.models import init_db
# if not os.path.exists("selfwebapp/site.db"):
#     init_db("admin", "password", ["data/Key.csv", "data/Loop.csv", "data/Social.csv", "data/Day.csv", "data/Status.csv"])

from selfwebapp import routes
