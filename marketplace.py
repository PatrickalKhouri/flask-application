from flask import Flask, render_template, url_for, flash, redirect  
from forms import RegistrationForm, LoginForm
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb+srv://Patrickdarya:dHtuTbVuJSRVt2L2@cluster0.g3erp.mongodb.net/mydb?retryWrites=true&w=majority"

mongo = PyMongo(app)
db = mongo.db
mycol = db["users"]

users_collection = db.users
products_collection = db.products

app.config['SECRET_KEY'] = '23b8868cf282837c556e88fd2c41cb'

products = []

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', products=products)
    

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        users_collection.insert_one({'username': form.username.data, 'email': form.email.data, 'password': form.password.data, 'admin': False })
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)