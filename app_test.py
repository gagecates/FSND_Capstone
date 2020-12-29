import os
import unittest
import flask_testing
import json
from flask_sqlalchemy import SQLAlchemy
from flask_testing import TestCase
from flask import session
from app import create_app, app
from dotenv import load_dotenv
from models import setup_db, Food, Macros, db_drop_and_create_all


load_dotenv()

database_path = os.environ.get('TEST_DATABASE_URL')

def get_headers(token):
    return {'Authorization': f'Bearer {token}'}


class MacroAppTestCase(TestCase):
    """This class represents the macro app test case"""

    def create_app(self):
        return app

    def setUp(self):
        """Define test variables and initialize app."""
        self.client = self.app.test_client
        self.database_name = "macro_test"
        self.database_path = database_path
        setup_db(self.app, self.database_path)


        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.admin = os.environ.get('admin_token')
        self.user = os.environ.get('user_token')

        self.new_user = Macros(
            user = 'Kevin',
            protein = 10,
            carbs = 5,
            fats = 5,
            calories = 5
        )

    
    # after each test revert changes
    def tearDown(self):
        """Executed after reach test"""
        pass


    def test_get_food(self): 
        res = self.client().get('/food', headers=get_headers(self.user))

        self.assertEqual(res.status_code, 200)
        self.assert_template_used('/pages/foods.html')


    def test_get_food_fail(self): 
        res = self.client().get('/food', headers=get_headers(''))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Token not found.')


    ''' Tested theses next four by using the username 'Kevin' instead of a session key username '''
    def test_get_macros(self): 
        res = self.client().get('/macros', headers=get_headers(self.user))

        self.assertEqual(res.status_code, 200)
        self.assert_template_used('pages/macro.html')

    
    def test_get_macros_fail(self): 
        res = self.client().get('/macros', headers=get_headers(''))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Token not found.')


    def test_add_food(self): 
        res = self.client().post('/food/add', data=dict(
            food='Chicken',
            servings=1
        ), headers=get_headers(self.user))

        self.assertEqual(res.status_code, 200)
        self.assert_template_used('/pages/macro.html')

    def test_add_food_fail(self): 
        res = self.client().post('/food/add', headers=get_headers(''))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Token not found.')


    def test_new_food(self): 
        res = self.client().post('/food/new', data=dict(
            food='Chicken',
        ), headers=get_headers(self.admin))

        self.assertEqual(res.status_code, 200)
        self.assert_template_used('forms/new_food.html')
        

    def test_new_food_fail(self): 
        res = self.client().post('/food/new', headers=get_headers(''))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Token not found.')


    def test_edit_food(self): 
        res = self.client().post('/food/3/edit', data=dict(
            protein=15,
            carbs=15,
            fats=15,
            calories=100,
        ), headers=get_headers(self.admin))

        self.assertEqual(res.status_code, 200)
        self.assert_template_used('/pages/foods.html')
        

    def test_edit_food_fail(self): 
        res = self.client().post('/food/1000/edit', headers=get_headers(self.admin))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')


    def test_delete_food(self):
        # create a new food to be deleted, then delete
        insert_food = Food(
                food = "Chicken",
                protein = 5,
                carbs = 1,
                fat = 1,
                calories = 1
            )

        insert_food.insert()
        # record number of foods before delete
        number_food = len(Food.query.all())

        # delete new food
        res = self.client().post(f'/food/{insert_food.id}/delete', headers=get_headers(self.admin))

        # record number of questions after delete
        number_food_new = len(Food.query.all())


        self.assertEqual(res.status_code, 200)
        self.assertEqual(number_food_new, number_food -1)
        self.assert_template_used('/pages/foods.html')


    def test_delete_food_fail(self):
        res = self.client().post('/food/1000/delete', headers=get_headers(self.admin))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')


    #Tested manually by assigning the session['user'] to 'Kevin'
    def test_manually_add_macros(self):
        res = self.client().post('/macros/add', data=dict(
            protein=15,
            carbs=15,
            fats=15,
            calories=100,
        ), headers=get_headers(self.admin))

        self.assertEqual(res.status_code, 200)
        self.assert_template_used('/pages/macro.html')


    def test_manually_add_macros_fail(self): 
        res = self.client().post('/macros/add', data=dict(
            protein=15,
            carbs=15,
            fats=15
        ), headers=get_headers(self.admin))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')
        

if __name__ == "__main__":
    unittest.main()