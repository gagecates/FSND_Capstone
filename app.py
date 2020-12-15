import os
from flask import Flask
from models import setup_db
from flask_cors import CORS
from models import Food

def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/')
    def list_foods():
        food = Food.query.all()
        if not food:
            abort(404)
        return food


    @app.route('/food', methods=['POST'])
    @requires_auth('post:drinks'))
    def be_cool():
        return "Be cool, man, be coooool! You're almost a FSND grad!"

    return app

app = create_app()

if __name__ == '__main__':
    app.run()