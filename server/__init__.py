from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from config import  Config

from os.path import  dirname


server_path = dirname(__file__)
project_path = dirname(server_path)
template_path = project_path + '/templates'


app = Flask(__name__, template_folder=template_path)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app,db)
login = LoginManager(app)
login.login_view = 'login'  # function that handles login ( whereto redirect)

bootstrap = Bootstrap(app)



from server import login_routes, models, petfeeder_routes

