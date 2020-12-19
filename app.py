import os
import json
import babel
from flask import Flask, request, jsonify, abort
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from models import setup_db
from flask_cors import CORS
from flask_wtf import Form
from logging import Formatter, FileHandler
from forms import *
from models import db_drop_and_create_all, Food, Macros
from auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

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


# home page -------------------------------------
@app.route('/')
def index():
  return render_template('/pages/home.html')


# get all foods from database -----------------
@app.route('/food', methods=['GET'])
def get_food():
    foods = Food.query.all()
    paged_foods = paginate_foods(request, foods)
    print(paged_foods)
    return render_template('/pages/foods.html', foods = paged_foods)
    
    return jsonify({
        'success': True,
        'foods': paged_foods
    })


# show current users macros -------------------
@app.route('/macros', methods=['GET'])
#@requires_auth('get:macros')
def get_macros():
    user = Macros.query.filter_by(user = "gage").first()
    if not user:
        abort(400)

    protein = user.protein
    carbs = user.carbs
    fats = user.fats
    calories = user.calories

    
    return jsonify({
        'success': True,
        'protein': protein,
        'carbs': carbs,
        'fats': fats,
        'calories': calories
    })

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
    


'''
User submits a food. If the food is not found need an error raised and a way to add to DB.
If the food is in the DB, its macros and calories get added to the users current macro and calorie count.
The users Macros are then updated in the DB.
'''
# consumed food submisison --------------------
@app.route('/food/add', methods=['PATCH'])
#@requires_auth('post:food')
def ate_food():
    user = Macros.query.filter_by(user = "Kevin").first()
    food_term = request.form["food"]
    servings = request.form['servings']
    food = Food.query.filter(Food.food.ilike(f'%{food_term}%')).first()
    if not food:
        flash('Looks like ' + request.form['food'] + ' was not found! You will have to add it to the databse')

    add_protein = int(user.protein) + int(food.protein)
    add_carbs = int(user.carbs) + int(food.carbs)
    add_fats = int(user.fats) + int(food.fat)
    add_calories = int(user.calories) + int(food.calories)

    user.user = user.user,
    user.protein = add_protein,
    user.carbs = add_carbs,
    user.fats = add_fats,
    user.calories = add_calories
    
    user.update()

    return jsonify({
        'success': True,
        'food': food_term,
        'protein': add_protein,
        'carbs': add_carbs,
        'fats': add_fats,
        'calories': add_calories
    })

# add a new food to the database ----------------
@app.route('/food/new', methods=['POST'])
#@requires_auth('post:new_food')
def new_food():
    data = request.get_json()
    new_food = Food(
        food = data['food'].lower(),
        protein = data['protein'],
        carbs = data['carbs'],
        fat = data['fats'],
        calories = data['calories']
    )

    new_food.insert()

    return jsonify({
        'success': True,
        'food': new_food.food,
        'message': "The food has been added"
    })

# manually submit macro information -------------
@app.route('/macros', methods=['POST'])
#@requires_auth('post:food')
def add_macros_manually():
    user = Macros.query.filter_by(user = "Kevin").first()
    data = request.get_json()
    if 'protein' and 'carbs' and 'fats' and 'calories' not in data:
        abort(400)
    
    add_protein = int(user.protein) + data['protein']
    add_carbs = int(user.carbs) + data['carbs']
    add_fats = int(user.fats) + data['fats']
    add_calories = int(user.calories) + data['calories']
    print(user.calories)
    user.user = user.user,
    user.protein = add_protein,
    user.carbs = add_carbs,
    user.fats = add_fats,
    user.calories = add_calories
    
    user.update()

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