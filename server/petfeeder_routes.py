from server import app, login
from flask_login import current_user, login_user, logout_user, login_required

from server.models import User
from server.forms import LoginForm
from flask import render_template, redirect, url_for, request, flash
from werkzeug.urls import url_parse


@app.route('/petfeeder')
@login_required
def petfeeder():
    return render_template('index.html',title= "petfeeder")