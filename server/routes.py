from server import app

from flask import render_template, redirect, url_for

@app.route('/')
def index():
    return render_template('index.html')