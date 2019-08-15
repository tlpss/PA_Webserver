from server import app, db
from server.models import User
# magic import...

from server.admin import  admin

#...
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}

if __name__ == "__main__":
    app.run(debug = True)