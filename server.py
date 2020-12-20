import os
from functools import wraps
import json
from os import environ as env
from werkzeug.exceptions import HTTPException

from dotenv import load_dotenv, find_dotenv
from flask import Flask
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for
from authlib.integrations.flask_client import OAuth
from six.moves.urllib.parse import urlencode

AUTH0_CALLBACK_URL = os.getenv('AUTH0_CALLBACK_URL')
AUTH0_CLIENT_ID = os.getenv('AUTH0_CLIENT_ID')
AUTH0_CLIENT_SECRET = os.getenv('AUTH0_CLIENT_SECRET')
AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
AUTH0_BASE_URL = os.getenv('AUTH0_BASE_URL')
AUTH0_AUDIENCE = os.getenv('AUTH0_AUDIENCE')

app = Flask(__name__)

oauth = OAuth(app)

auth0 = oauth.register(
    'auth0',
    client_id='zeu5Q4B8xrU7BymT7dxwW7VTh6To2chH',
    client_secret='L7c1jjyvy9nsdExxng77bd0Oahiin0aYOqWueqLE_WVxIHSeoPIliU-FQHk5sq8K',
    api_base_url='https://fnsd-gmc.us.auth0.com',
    access_token_url='https://fnsd-gmc.us.auth0.com/oauth/token',
    authorize_url='https://fnsd-gmc.us.auth0.com/authorize',
    client_kwargs={
        'scope': 'openid profile email',
    },
)
