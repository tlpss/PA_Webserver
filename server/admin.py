from server import  app
from server.models import *
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import  current_user
from flask import redirect, url_for, flash, request

class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.admin
    def inaccessible_callback(self, name, **kwargs):
        flash("please login with an admin account to access the admin section")
        return redirect(url_for('login',next = 'admin'))

#TODO: facilitate creation by entering plain text keys instead of hashes
class MyIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.admin
    def inaccessible_callback(self, name, **kwargs):
        flash("please login with an admin account to access the admin section")
        return redirect(url_for('login',next = 'admin'))

admin = Admin(app, name='PetFeeder', template_mode='bootstrap3', index_view=MyIndexView())
admin.add_view(MyModelView(User,db.session))
admin.add_view(MyModelView(Feeder,db.session))
admin.add_view(MyModelView(FeedMoment,db.session))

