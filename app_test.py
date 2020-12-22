import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import exists
from flaskr import create_app
from models import setup_db, Food, Macros


Admin_Token = 
User_Token = 



def get_headers(token):
    return {'Authorization': f'Bearer {token}'}


class MacroAppTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "macro_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            'question': 'Who was the first President of the United States?',
            'answer': 'George Washington',
            'difficulty': 1,
            'category': '3'
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    
    # after each test revert changes
    def tearDown(self):
        """Executed after reach test"""
        pass


    def get_food(self): 
        res = self.client().get('/food', headers=get_headers(User))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def get_food_fail(self): 
        res = self.client().get('/food', headers=get_headers(''))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        

    def test_delete_question(self):
        # create a new food to be deleted, then delete
        food = Food(
                food = "Steak",
                protein = 5,
                carbs = 1,
                fat = 1,
                calories = 1
            )

        food.insert()
        food_id = food.id

        # record number of foods before delete
        number_food = len(Food.query.all())

        # delete new food
        res = self.client().delete(f'/food/{food_id}/delete')
        data = json.loads(res.data)

        # record number of questions after delete
        number_food_new = len(Food.query.all())

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(number_food_new, number_food -1)


    def test_delete_question_fail(self):
        # create a new food to be deleted, then delete
        food = Food(
                food = "Steak",
                protein = 5,
                carbs = 1,
                fat = 1,
                calories = 1
            )

        food.insert()
        food_id = 100

        # record number of foods before delete
        number_food = len(Food.query.all())

        # delete new food
        res = self.client().delete(f'/food/{food_id}/delete')
        data = json.loads(res.data)

        # record number of questions after delete
        number_food_new = len(Food.query.all())

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)


    def test_question_search_404(self):

        # test using a funky entry for a search
        search_terms = {
            'searchTerm': '8675309',
        }

        res = self.client().post('/questions/search', json=search_terms)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_page_out_of_range_400(self):

        # send request for out of range page number
        response = self.client().get('/questions?page=100')
        data = json.loads(response.data)

        # check response status code and message
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

# Make the tests conveniently executable

if __name__ == "__main__":
    unittest.main()