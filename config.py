import os
from app import app
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

