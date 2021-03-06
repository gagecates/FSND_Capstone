import os
import json
import babel
import requests
import constants
from flask import Flask, request, jsonify, abort, session, make_response
from flask import render_template, Response, flash, redirect, url_for
from models import setup_db
from flask_cors import CORS, cross_origin
from flask_wtf import Form
from logging import Formatter, FileHandler
from forms import *
from models import db_drop_and_create_all, Food, Macros
from auth import AuthError, requires_auth
from sqlalchemy.sql import exists
from models import db
from server import *


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization,true')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    # SECRET_KEY = 'os.urandom(32)' / cannot use a random key or will throw
    # errors.
    SECRET_KEY = os.environ.get('SECRET_KEY')
    app.config['SECRET_KEY'] = SECRET_KEY

    # db_drop_and_create_all()
    # Use this only for initial table creation on initialization.

    Foods_Per_Page = 10
    # page pagination -----------------------------

    def paginate_foods(request, all_foods):

        page = request.args.get('page', 1, type=int)
        start = (page - 1) * Foods_Per_Page
        end = start + Foods_Per_Page

        foods = [food.format() for food in all_foods]
        page_foods = foods[start:end]

        return page_foods

    # login page -------------------------------------

    @app.route('/')
    def home():
        if 'user' in session:
            return render_template(
                '/pages/app_home.html',
                user=session['user'])
        else:
            return render_template('/pages/app_login.html')

    # redirects to auth 0 login ----------------------

    @app.route('/login')
    def login():
        # return
        # auth0.authorize_redirect(redirect_uri='https://gage-heroku-app.herokuapp.com/callback',_external=True,
        # audience = AUTH0_AUDIENCE)
        return auth0.authorize_redirect(
            redirect_uri='https://gage-heroku-app.herokuapp.com/callback',
            _external=True,
            audience=AUTH0_AUDIENCE)

    # auth0 login callback ----------------------------
    @app.route('/callback', methods=['GET'])
    def callback_handling():
        auth = auth0.authorize_access_token()
        user = auth0.get('userinfo')
        userinfo = user.json()
        # store jwt in session
        session['token'] = auth['access_token']
        # store username in session
        session['user'] = userinfo['name']

        user_exits = Macros.query.filter_by(user=session['user']).first()

        if not user_exits:
            add_user = Macros(
                user=session['user'],
                protein=0,
                carbs=0,
                fats=0,
                calories=0
            )

            add_user.insert()

        return render_template('pages/app_home.html', user=session['user'])

    # auth0 logout. Redirects to login page ---------

    @app.route('/logout')
    def log_out():
        # clear the session
        session.clear()
        # redirect user to logout endpoint
        params = {
            'returnTo': url_for(
                'home',
                _external=True),
            'client_id': AUTH0_CLIENT_ID}
        return redirect(
            'https://fnsd-gmc.us.auth0.com' +
            '/v2/logout?' +
            urlencode(params))

    # get all foods from database -----------------

    @app.route('/food', methods=['GET'])
    @requires_auth('get:foods')
    def get_food(payload):
        foods = Food.query.all()
        paged_foods = paginate_foods(request, foods)
        if len(paged_foods) == 0:

            flash('Looks like you need to add some food first!')
            return render_template(
                '/pages/app_home.html',
                user=session['user'])

        return render_template('/pages/foods.html', foods=paged_foods)

    # show current users macros -------------------

    @app.route('/macros', methods=['GET'])
    @requires_auth('get:macros')
    def get_macros(payload):
        username = session['user']
        # username = 'Kevin' / this is used for unittesting when there is no
        # session user.
        user = Macros.query.filter_by(user=username).first()
        if not user:
            abort(400)

        protein = user.protein
        carbs = user.carbs
        fats = user.fats
        calories = user.calories

        return render_template(
            'pages/macro.html',
            user=user,
            username=username)

    # get new food form --------------------------

    @app.route('/food/add', methods=['GET'])
    @requires_auth('post:food')
    def food_add_form(payload):
        form = PostFood()
        return render_template('forms/post_food.html', form=form)

    # get add macros form ------------------------

    @app.route('/macros/add', methods=['GET'])
    @requires_auth('post:macros')
    def macros_add_form(payload):
        form = PostMacros()
        return render_template('forms/post_macros.html', form=form)

    # consumed food submisison --------------------

    @app.route('/food/add', methods=['POST'])
    @requires_auth('post:food')
    def ate_food(payload):
        username = session['user']
        # username = 'Kevin'/ this is used for unittesting when there is no
        # session user.
        form = PostFood()
        user = Macros.query.filter_by(user=username).first()
        food_term = request.form["food"]
        servings = request.form['servings']
        food = Food.query.filter(Food.food.ilike(f'%{food_term}%')).first()
        if not food:
            flash(
                'Looks like ' +
                request.form['food'] +
                ' was not found! Try again or add it to the database')
            return render_template('forms/post_food.html', form=form)

        add_protein = int(user.protein) + (int(food.protein) * int(servings))
        add_carbs = int(user.carbs) + (int(food.carbs) * int(servings))
        add_fats = int(user.fats) + (int(food.fat) * int(servings))
        add_calories = int(user.calories) + \
            (int(food.calories) * int(servings))

        user.user = user.user,
        user.protein = add_protein,
        user.carbs = add_carbs,
        user.fats = add_fats,
        user.calories = add_calories

        user.update()

        flash('Your macros have been updated!')
        return render_template('/pages/macro.html', user=user)

    # get new food form ----------------------------

    @app.route('/food/new', methods=['GET'])
    @requires_auth('post:new-food')
    def get_new_food_form(payload):
        form = NewFood()
        return render_template('forms/new_food.html', form=form)

    # add a new food to the database ----------------

    @app.route('/food/new', methods=['POST'])
    @requires_auth('post:new-food')
    def new_food(payload):
        foods = Food.query.all()
        form = NewFood()
        current_foods = Food.query.all()
        if db.session.query(
            exists().where(
                Food.food == request.form['food'])).scalar():
            flash('Looks like that food is already in our database.')

            return render_template('forms/new_food.html', form=form)

        new_food = Food(
            food=request.form['food'].lower(),
            protein=request.form['protein'],
            carbs=request.form['carbs'],
            fat=request.form['fats'],
            calories=request.form['calories']
        )

        new_food.insert()

        current_foods = Food.query.all()
        paged_foods = paginate_foods(request, current_foods)
        print(paged_foods)
        flash(request.form['food'] + ' has been successfully added!')
        return render_template('/pages/foods.html', foods=paged_foods)

    # get edit food form -----------------

    @app.route('/food/<int:food_id>/edit', methods=['GET'])
    @requires_auth('patch:food')
    def edit_food_form(payload, food_id):
        form = EditFood()
        food = Food.query.get(food_id)
        return render_template(
            'forms/edit_food.html',
            form=form,
            food=food.food)

    # edit food in databae ----------------

    @app.route('/food/<int:food_id>/edit', methods=['POST'])
    @requires_auth('patch:food')
    def edit_food(payload, food_id):
        food = Food.query.get(food_id)
        if not food:
            abort(404)

        food.protein = request.form['protein']
        food.carbs = request.form['carbs']
        food.fats = request.form['fats']
        food.calories = request.form['calories']

        food.update()

        flash(food.food + ' has been successfully updated!')

        foods = Food.query.all()
        paged_foods = paginate_foods(request, foods)

        return render_template('/pages/foods.html', foods=paged_foods)

    # delete food in databae ----------------

    @app.route('/food/<int:food_id>/delete', methods=['POST'])
    @requires_auth('delete:food')
    def delete_food(payload, food_id):
        food = Food.query.get(food_id)
        if not food:
            abort(404)

        food.delete()

        flash(food.food + ' has been successfully deleted!')

        foods = Food.query.all()
        paged_foods = paginate_foods(request, foods)

        return render_template('/pages/foods.html', foods=paged_foods)

    # manually submit macro information -------------

    @app.route('/macros/add', methods=['POST'])
    @requires_auth('post:macros')
    def add_macros_manually(payload):
        username = session['user']
        # username = 'Kevin' / this is used for unittesting when there is no
        # session user.
        user = Macros.query.filter_by(user=username).first()
        if 'protein' and 'carbs' and 'fats' and 'calories' not in request.form:
            abort(400)

        add_protein = int(user.protein) + int(request.form['protein'])
        add_carbs = int(user.carbs) + int(request.form['carbs'])
        add_fats = int(user.fats) + int(request.form['fats'])
        add_calories = int(user.calories) + int(request.form['calories'])
        user.user = user.user,
        user.protein = add_protein,
        user.carbs = add_carbs,
        user.fats = add_fats,
        user.calories = add_calories

        user.update()

        flash('Your macros have been successfully updated!')
        return render_template('/pages/macro.html', user=user)

    # error handling ---------------------------

    @app.errorhandler(400)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'

        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'

        }), 404

    @app.errorhandler(422)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'

        }), 422

    @app.errorhandler(AuthError)
    def authentification_failed(AuthError):
        return json.dumps({
            'success': False,
            'error': AuthError.status_code,
            'message': AuthError.error['description']
        }), AuthError.status_code

    return app


app = create_app()


if __name__ == '__main__':
    app.run()
