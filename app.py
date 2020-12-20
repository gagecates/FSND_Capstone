import os
import json
import babel
import requests
from flask import Flask, request, jsonify, abort
from flask import Flask, render_template, request, Response, flash, redirect, url_for
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

app = Flask(__name__)
setup_db(app)
CORS(app)

@app.after_request
def after_request(response):
	response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
	response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
	return response


SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

# run function below upon initial startup to initialize tables. Delete/comment out after creation. 
#db_drop_and_create_all()
'''
name = "James"
my_protein = 50
my_carbs = 10
my_fats = 100
my_calories = 200
new_item = Macros(
    user = name, 
    protein = my_protein, 
    carbs = my_carbs, 
    fats = my_fats, 
    calories = my_calories
)
new_item.insert()
'''
add_food = "chips"
add_protein = 50
add_carbs = 100
add_fats = 20
add_calories = 200

new_food = Food(
    food = add_food,
    protein = add_protein,
    carbs = add_carbs,
    fat = add_fats,
    calories = add_calories
)
#new_food.insert()


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
@cross_origin()
def index():
  return render_template('/pages/app_login.html')


@app.route('/login')
@cross_origin()
def login():
    return auth0.authorize_redirect(redirect_uri='https://localhost:5000/callback')

@app.route('/callback', methods=['GET'])
@cross_origin()
def callback_handling():
    print('aye')
    # Handles response from token endpoint
    token = auth0.authorize_access_token()
    session['token'] = token['access_token']
    print(session['token'])
    return render_template('pages/app_home.html')


# home page -------------------------------------
@app.route('/homes')
def home_page():
  return render_template('/pages/app_home.html')


# get all foods from database -----------------
@app.route('/food', methods=['GET'])
def get_food():
    foods = Food.query.all()
    paged_foods = paginate_foods(request, foods)
    return render_template('/pages/foods.html', foods = paged_foods)


# show current users macros -------------------
@app.route('/macros', methods=['GET'])
#@requires_auth('get:macros')
def get_macros():
    user = Macros.query.filter_by(user = "Kevin").first()
    if not user:
        abort(400)

    protein = user.protein
    carbs = user.carbs
    fats = user.fats
    calories = user.calories

    return render_template('pages/macro.html', user = user)

# get individual food details -------------------
@app.route('/food<int:food_id>', methods=['GET'])
#@requires_auth('get:macros')
def get_food_details(food_id):
    food = Food.query.get(food_id)
    if not food:
        abort(404)


@app.route('/food/add', methods=['GET'])
def food_add_form():
    form = PostFood()
    return render_template('forms/post_food.html', form=form)


@app.route('/macros/add', methods=['GET'])
def macros_add_form():
    form = PostMacros()
    return render_template('forms/post_macros.html', form=form)
    


'''
User submits a food. If the food is not found need an error raised and a way to add to DB.
If the food is in the DB, its macros and calories get added to the users current macro and calorie count.
The users Macros are then updated in the DB.
'''
# consumed food submisison --------------------
@app.route('/food/add', methods=['POST'])
#@requires_auth('post:food')
def ate_food():
    form = PostFood()
    user = Macros.query.filter_by(user = "Kevin").first()
    food_term = request.form["food"]
    servings = request.form['servings']
    food = Food.query.filter(Food.food.ilike(f'%{food_term}%')).first()
    if not food:
        flash('Looks like ' + request.form['food'] + ' was not found! Try again or add it to the database')
        return render_template('forms/post_food.html', form=form)

    add_protein = int(user.protein) + (int(food.protein) * int(servings))
    add_carbs = int(user.carbs) + (int(food.carbs) * int(servings))
    add_fats = int(user.fats) + (int(food.fat) * int(servings))
    add_calories = int(user.calories) + (int(food.calories) * int(servings))

    user.user = user.user,
    user.protein = add_protein,
    user.carbs = add_carbs,
    user.fats = add_fats,
    user.calories = add_calories
    
    user.update()

    flash('Your macros have been updated!')
    return render_template('/pages/macro.html', user= user)


# get new food form -----------------
@app.route('/food/new', methods=['GET'])
def get_new_food_form():
    form = NewFood()
    return render_template('forms/new_food.html', form=form)


# add a new food to the database ----------------
@app.route('/food/new', methods=['POST'])
#@requires_auth('post:new_food')
def new_food():
    foods = Food.query.all()
    paged_foods = paginate_foods(request, foods)
    form = NewFood()
    current_foods = Food.query.all()
    if db.session.query(exists().where(Food.food == request.form['food'])).scalar():
        flash('Looks like that food is already in our database.')
        return render_template('forms/new_food.html', form = form)
       
    new_food = Food(
        food = request.form['food'].lower(),
        protein = request.form['protein'],
        carbs = request.form['carbs'],
        fat = request.form['fats'],
        calories = request.form['calories']
    )

    new_food.insert()

    flash(request.form['food'] + ' has been successfully added!')
    return render_template('/pages/foods.html', foods = paged_foods)
    
    return jsonify({
        'success': True,
        'food': new_food.food,
        'message': "The food has been added"
    })


# get edit food form -----------------
@app.route('/food/<int:food_id>/edit', methods=['GET'])
def edit_food_form(food_id):
    form = EditFood()
    food = Food.query.get(food_id)
    return render_template('forms/edit_food.html', form=form, food = food.food)


# edit food in databae ----------------
@app.route('/food/<int:food_id>/edit', methods=['POST'])
#@requires_auth('post:new_food')
def edit_food(food_id):
    food = Food.query.get(food_id)

    food.protein = request.form['protein']
    food.carbs = request.form['carbs']
    food.fats = request.form['fats']
    food.calories = request.form['calories']
    
    update_food.update()

    flash(food.food + ' has been successfully updated!')

    foods = Food.query.all()
    paged_foods = paginate_foods(request, foods)
    return render_template('/pages/foods.html', foods = paged_foods)
    
    return jsonify({
        'success': True,
        'food': new_food.food,
        'message': "The food has been added"
    })

# delete food in databae ----------------
@app.route('/food/<int:food_id>', methods=['POST'])
#@requires_auth('post:new_food')
def delete_food(food_id):
    food = Food.query.get(food_id)
    print(food)
    if not food:
        abort(404)

    food.delete()

    flash(food.food + ' has been successfully deleted!')

    foods = Food.query.all()
    paged_foods = paginate_foods(request, foods)
    return render_template('/pages/foods.html', foods = paged_foods)
    
    return jsonify({
        'success': True,
        'food': new_food.food,
        'message': "The food has been added"
    })

# manually submit macro information -------------
@app.route('/macros/add', methods=['POST'])
#@requires_auth('post:food')
def add_macros_manually():
    user = Macros.query.filter_by(user = "Kevin").first()
    if 'protein' and 'carbs' and 'fats' and 'calories' not in request.form:
        abort(400)
    add_protein = int(user.protein) + int(request.form['protein'])
    add_carbs = int(user.carbs) + int(request.form['carbs'])
    add_fats = int(user.fats) + int(request.form['fats'])
    add_calories = int(user.calories) + int(request.form['calories'])
    print(user.calories)
    user.user = user.user,
    user.protein = add_protein,
    user.carbs = add_carbs,
    user.fats = add_fats,
    user.calories = add_calories
    
    user.update()

    flash('Your macros have been successfully updated!')
    return render_template('/pages/macro.html', user= user)

    return jsonify({
        'success': True,
        'protein': add_protein,
        'carbs': add_carbs,
        'fats': add_fats,
        'calories': add_calories
    })


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



if __name__ == '__main__':
    app.run()