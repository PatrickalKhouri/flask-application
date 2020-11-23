import os
from flask import Flask
from uuid import uuid4
from flask_login import UserMixin
from flask_bcrypt import Bcrypt
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://Patrickdarya:dHtuTbVuJSRVt2L2@cluster0.g3erp.mongodb.net/mydb?retryWrites=true&w=majority"
app.config['SECRET_KEY'] = '23b8868cf282837c556e88fd2c41cb'
bcrypt = Bcrypt(app)
mongo = PyMongo(app)
db = mongo.db
users_collection = db.users


class User(UserMixin):
    def __init__(self, obj):
        self.username = obj['username']
        self.email = obj['email']
        self.password = obj['password']
        self.admin = False if 'admin' not in obj.keys() else obj['admin']
        self.uuid = str(uuid4()) if 'uuid' not in obj.keys() else obj['uuid']

    def get_id(self):
        return self.uuid

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    @staticmethod
    def generate_id():
        return str(uuid4())

    def save(self):
        user_id = users_collection.insert_one(
            {'uuid': self.generate_id(), 'username': self.username, 'email': self.email,
             'password': self.password, 'admin': self.admin})
        return user_id
