import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json


database_path = os.environ['DATABASE_URL']
database_name = 'capstone'
# database_path = "postgres://{}/{}".format('localhost:5432', database_name)


db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


# models -----------------------------------------

# food --------------------
class Food(db.Model):
    __tablename__ = 'Food'

    id = db.Column(Integer, primary_key=True)
    food = db.Column(String)
    protein = db.Column(Integer)
    carbs = db.Column(Integer)
    fat = db.Column(Integer)
    calories = db.Column(Integer)

    def __init__(self, food, protein, carbs, fat, calories):
        self.food = food
        self.protein = protein
        self.carbs = carbs
        self.fat = fat
        self.calories = calories

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'food': self.food,
            'protein': self.protein,
            'carbs': self.carbs,
            'fat': self.fat,
            'calories': self.calories
        }


# macros ----------------
class Macros(db.Model):
    __tablename__ = 'Macros'

    id = db.Column(Integer, primary_key=True)
    user = db.Column(String)
    protein = db.Column(Integer)
    carbs = db.Column(Integer)
    fats = db.Column(Integer)
    calories = db.Column(Integer)

    def __init__(self, user, protein, carbs, fats, calories):
        self.user = user
        self.protein = protein
        self.carbs = carbs
        self.fats = fats
        self.calories = calories

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
