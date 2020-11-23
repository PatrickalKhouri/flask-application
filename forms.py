import os

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from flask_pymongo import PyMongo
from flask import Flask

app = Flask(__name__)
app.config["MONGO_URI"] = os.environ.get('DB_URL')
mongo = PyMongo(app)
db = mongo.db
users_collection = db.users

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(),])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    picture = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = users_collection.find({"username": username.data}).count()
        if user:
            raise ValidationError('Username already exists')

    def validate_email(self, email):
        email = users_collection.find({"email": email.data}).count()
        if email:
            raise ValidationError('Email already exists')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class ProductForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    editor = StringField('Editor', validators=[DataRequired()])
    year_published = StringField('Year Published', validators=[DataRequired(), Length(max=4)])
    price = IntegerField('Price', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    summary = TextAreaField('Summary', validators=[DataRequired(), Length(min=20, max=500)])
    cover = FileField('Cover', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Add book')
