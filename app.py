import os
import json
from flask import Flask, jsonify, abort
from models import setup_db
from flask_cors import CORS
from models import db_drop_and_create_all, Food, Macros

app = Flask(__name__)
setup_db(app)
CORS(app)

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

'''
User submits a food. If the food is not found need an error raised and a way to add to DB.
If the food is in the DB, its macros and calories get added to the users current macro and calorie count.
The users Macros are then updated in the DB using a POSTcommand.

'''

@app.route('/food', methods=['POST'])
#@requires_auth('post:food')
def add_food():
    user = Macros.query.filter_by(user = "gage").first()
    data = request.get_json()
    if 'food' not in data:
        return ({
            'success': False,
            'message': "Looks like that food is not saved. You will need to add it."
        })
    
    food = Food.query.filter_by(food = data['food'].lower()).first()

    user_protein = user.protein
    user_carbs = user.carbs
    user_fats = user.fats
    user_calories = user.calories

    food_protein = food.protein
    food_carbs = food.carbs
    food_fats = food.fats
    food_calories = food.calories

    add_protein = user_protein + food_protein
    add_carbs = user_carbs + food_carbs
    add_fats = user_fats + food_fats
    add_calories = user_calories + food_calories

    update_user = Macros(
        protein = add_protein,
        carbs = add_carbs,
        fats = add_fats,
        calories = add_calories
        )
    update_user.update()

    return jsonify({
        'success': True,
        'food': food,
        'protein': add_protein,
        'carbs': add_carbs,
        'fats': add_fats,
        'calories': add_calories
    })
    

@app.route('/food/new', methods=['POST'])
#@requires_auth('post:new_food')
def new_food(payload):
    data = request.get_json()
    new_food = Food(
        food = data.food.lower(),
        protein = data.protein,
        carbs = data.carbs,
        fats = data.fats,
        calories = data.calories
    )

    new_food.insert()

    return jsonify({
        'success': True,
        'food': new_food,
        'message': "The food has been added"
    })


@app.route('/macros', methods=['POST'])
#@requires_auth('post:food')
def add_macros_manually():
    user = Macros.query.filter_by(user = "gage").first()
    data = request.get_json()
    if 'food' not in data:
        abort(404)
    
    user_protein = user.protein
    user_carbs = user.carbs
    user_fats = user.fats
    user_calories = user.calories

    food_protein = data.protein
    food_carbs = data.carbs
    food_fats = data.fats
    food_calories = data.calories

    add_protein = user_protein + food_protein
    add_carbs = user_carbs + food_carbs
    add_fats = user_fats + food_fats
    add_calories = user_calories + food_calories

    update_user = Macros(
        protein = add_protein,
        carbs = add_carbs,
        fats = add_fats,
        calories = add_calories
        )

    update_user.update()

    return jsonify({
        'success': True,
        'protein': add_protein,
        'carbs': add_carbs,
        'fats': add_fats,
        'calories': add_calories
    })



if __name__ == '__main__':
    app.run()