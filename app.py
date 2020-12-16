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
# db_drop_and_create_all()

'''
name = "gage"
macros = 50
calories = 200
new_item = Macros(user = name, macros = macros, calories = calories)
new_item.insert()
'''

@app.route('/macros', methods=['GET'])
#@requires_auth('get:macros')
def get_macros():
    user = Macros.query.filter_by(user = "gage").first()
    if not user:
        abort(404)

    protein = user.protein
    carbs = user.carbs
    fats = user.fats
    calories = calories

    
    return jsonify({
        'success': True,
        'protein': protein
        'carbs': carbs
        'fats': fats
        'calories': calories
    })

'''
User submits a food. If the food is not found need an error raised and a way to add to DB.
If the food is in the DB, its macros and calories get added to the users current macro and calorie count.
The users Macros are then updated in the DB using a PATCH command.

'''

@app.route('/macros', methods=['PATCH'])
#@requires_auth('post:food')
def add_food():
    user = Macros.query.filter_by(user = "gage").first()
    data = request.get_json()
    if 'food' not in data:
        abort(404)
    
    food = Food.query.filter_by(food = data['food'])first()

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
        protein = add_protein
        carbs = add_carbs
        fats = add_fats
        calories = add_calories
        )
    update_user.update()



    return jsonify({
        'success': True,
        'macros': macros
    })

if __name__ == '__main__':
    app.run()