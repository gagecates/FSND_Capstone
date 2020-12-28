import json
import os
from flask import request, _request_ctx_stack, session, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen
from os import environ
from server import *

AUTH0_DOMAIN = 'fnsd-gmc.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'Macros'

#Auth0_login = 'https://fnsd-gmc.us.auth0.com/authorize?audience=Macros&response_type=token&client_id=zeu5Q4B8xrU7BymT7dxwW7VTh6To2chH&redirect_uri=https://localhost:5000/home'

#bearer_tokens = {
# "user" : "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik16azVRVUk0TXpSR04wSXhOVU13TkRrME16QXdNMFpHTmtFMU1VWXdPRUpCTmpnMFJrVTBSZyJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtbWF0dGhldy5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU0N2VmNTg3ZWY5YjEwZjA0ZmQ5M2MzIiwiYXVkIjoiTXVzaWMiLCJpYXQiOjE1ODE4NDUzNjksImV4cCI6MTU4MTg1MjU2OSwiYXpwIjoiVGh2aG9mdmtkRTQwYlEzTkMzSzdKdFdSSzdSMzFOZDciLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbInJlYWQ6YWN0b3JzIiwicmVhZDptb3ZpZXMiXX0.wxurZHZR-Y8o-8q8vfEgROiJjksN4LXfE0yWJZM-MpkJBQspwUqS6MUus_-qWC5Qn8BnHgfQNxx7WVpvax81Isloty1VwfwtgqKeua66oRc9999FYPftmT-CZmIkVB3bEqNB_fhFF8y3t4Vy2QoFmAvGV74TJVnCbsrQdxWmJENyL-ubABPPEJyKbUdKumB-dgIu7PIqVHp4Weclr6xYpB4buuhO4X4G37dS3Nzy1TSRmuRD4IotlE1FQBj7t3a9lfu5wNbReWsCHBd-Ptubw_ivdb4u4wC6jkgCoCT8tBQs9nS6XHlj-35tEwisnEMah4-RcswXAKi4CJ19MoE4tA",
#  "admin" : "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik16azVRVUk0TXpSR04wSXhOVU13TkRrME16QXdNMFpHTmtFMU1VWXdPRUpCTmpnMFJrVTBSZyJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtbWF0dGhldy5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU0N2VmYzc2N2YxYmEwZWJiNDIwMTYzIiwiYXVkIjoiTXVzaWMiLCJpYXQiOjE1ODE4NDUzMTUsImV4cCI6MTU4MTg1MjUxNSwiYXpwIjoiVGh2aG9mdmtkRTQwYlEzTkMzSzdKdFdSSzdSMzFOZDciLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImNyZWF0ZTphY3RvcnMiLCJjcmVhdGU6bW92aWVzIiwiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJlZGl0OmFjdG9ycyIsImVkaXQ6bW92aWVzIiwicmVhZDphY3RvcnMiLCJyZWFkOm1vdmllcyJdfQ.xNig8PxzNbOC0XXdQeXKE92eMG4qcOy-3eG9vuvwZtgw4adcVzi9tIObI5HwhFDdbgczd7EQZBRHAYLUZk5J-vGk6Ba0-uzYBN1VF3MLLQpmh3WW50Sbdr9Sjhs1OIDN7FMMy7tCiwGqIaxFwIpUX-5BAHFrtEEnsFlCPi5j784GCGr3KFa9HNzX9o4dcsGWURldr_5PDxWFcR8IXLJHUzmb6az_zP8UEQP8hUVzY3B3HwaFGWJG5nfEaNr6sLGosnfCW2wcZ0a311KgAZfA5WXsSl0WVSRNpHvjruv1dF7tHEdZJt1dMEJGnWP6ei8lyDDHoIkvSa64TZPa_5Ikgg",


## AuthError Exception

class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


## Auth Header

def get_token_auth_header():
    auth = request.headers.get('Authorization', None)
    if not auth:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }, 401)

    parts = auth.split()
    if parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)

    elif len(parts) == 1:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found.'
        }, 401)

    elif len(parts) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token.'
        }, 401)

    token = parts[1]
    return token


def check_permissions(permission, payload):
    if 'permissions' not in payload:
            abort(400)

    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission Not found',
        }, 401)
    return True
        

def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 401)


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = None
            if 'token' in session:
                token = session['token']
            else:
                token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator