from server import app, db
from server.models import User
# magic import
# IMPORTANT , in production this import must be done in the WSGI file because this run.py isn't the entry point anymore

from server.admin import  admin

#...
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}

if __name__ == "__main__":
    app.run(debug = True)