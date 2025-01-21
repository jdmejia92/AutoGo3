from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask import Flask

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
app = Flask(__name__)
