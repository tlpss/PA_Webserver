from server import  app
from server.models import *
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

admin = Admin(app, name='PetFeeder', template_mode='bootstrap3')
admin.add_view(ModelView(User,db.session))