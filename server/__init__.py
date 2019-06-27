from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import  Config

from os.path import  dirname


server_path = dirname(__file__)
project_path = dirname(server_path)
template_path = project_path + '/templates'


app = Flask(__name__, template_folder=template_path)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app)

from server import routes, models