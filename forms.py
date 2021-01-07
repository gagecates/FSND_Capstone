from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SelectField, BooleanField, DateTimeField
from wtforms import ValidationError, IntegerField, SelectMultipleField
from wtforms.validators import DataRequired, AnyOf, URL, Length


class PostFood(Form):
    food = StringField(
        'name', validators=[DataRequired()]
    )
    servings = IntegerField(
        'servings', validators=[DataRequired()],
    )


class PostMacros(Form):
    calories = IntegerField(
        'caloties', validators=[DataRequired()]
    )
    protein = IntegerField(
        'protein', validators=[DataRequired()]
    )
    carbs = IntegerField(
        'carbs', validators=[DataRequired()]
    )
    fats = IntegerField(
        'fats', validators=[DataRequired()]
    )


class NewFood(Form):
    food = StringField(
        'food', validators=[DataRequired()]
    )
    calories = IntegerField(
        'calories', validators=[DataRequired()]
    )
    protein = IntegerField(
        'protein', validators=[DataRequired()]
    )
    carbs = IntegerField(
        'carbs', validators=[DataRequired()]
    )
    fats = IntegerField(
        'fats', validators=[DataRequired()]
    )


class EditFood(Form):
    calories = IntegerField(
        'calories', validators=[DataRequired()]
    )
    protein = IntegerField(
        'protein', validators=[DataRequired()]
    )
    carbs = IntegerField(
        'carbs', validators=[DataRequired()]
    )
    fats = IntegerField(
        'fats', validators=[DataRequired()]
    )
