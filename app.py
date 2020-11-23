import logging

from uuid import uuid4

from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm, ProductForm
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, logout_user, login_required
from models import User
from logging import FileHandler, WARNING

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://Patrickdarya:dHtuTbVuJSRVt2L2@cluster0.g3erp.mongodb.net/mydb?retryWrites=true&w=majority"
mongo = PyMongo(app)
db = mongo.db
users_collection = db.users
products_collection = db.products
app.config['SECRET_KEY'] = '23b8868cf282837c556e88fd2c41cb'
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
file_hander = FileHandler('errorlog.txt')
file_hander.setLevel(WARNING)

app.logger.setLevel(logging.DEBUG)

@login_manager.user_loader
def load_user(user_id):
	return None


@app.route('/')
@app.route('/home')
def home():
    products = products_collection
    return render_template('home.html', products=products)
    

@app.route('/about')
def about():
    return render_template('about.html', title='About')


@login_manager.user_loader
def load_user(user_id):
    try:
        user = User(users_collection.find_one({"uuid": user_id}))
        return user
    except:
        return None


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(form.data)
        user.set_password(form.data['password'])
        user.save()
        #users_collection.insert_one({'uuid': uuid4().int, 'username': form.username.data, 'email': form.email.data, 'password': hashed_password, 'admin': False })
        flash('Your account has been created! You are now able to log in', 'success')
        app.logger.info('New user created sucessfully')
        return redirect(url_for('login'))
    else:
        app.logger.info('New user not created, error')
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = users_collection.find_one({"email": form.email.data})
        if user:
            user = User(user)
        else:
            app.logger.info('User not found.')
        if user and user.check_password(form.password.data.encode('utf-8')):
            login_user(user, remember=form.remember.data)
            app.logger.info('Login Sucessfull')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
            app.logger.info('Login Failed')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
    image_file = url_for('static', filename='user_images/avatar.jpg')
    return render_template('account.html', title='Account', image_file=image_file)


@app.route("/products/new", methods=['GET', 'POST'])
def new_product():
    form = ProductForm()
    if form.validate_on_submit():
         products_collection.insert_one({'title': form.title.data, 'author': form.author.data, 'editor': form.editor.data, 
                                        'year_published': form.year_published.data, 'price': form.price.data , 'quantity': form.quantity.data,
                                        'summary': form.summary.data})
         flash('Product created!', 'success')
         app.logger.info('Product Created Sucessfully')
         return redirect(url_for('home'))
    else: 
        app.logger.info('PRODUCT NOT CREATED, ERROR')
    return render_template('create_product.html', title='New Product', form=form, legend="Update Product")


@app.route("/product/<product_title>")
def product(product_title):
    product =  products_collection.find_one({"title": product_title})
    return render_template('product.html', title=product["title"], product=product)


@app.route("/product/<product_title>/update", methods=['GET', 'POST'])
@login_required
def update_product(product_title):
    product =  products_collection.find_one({"title": product_title})
    form = ProductForm()
    if form.validate_on_submit():
         products_collection.update( products_collection.find_one({"title": product_title}), {'title': form.title.data, 'author': form.author.data, 'editor': form.editor.data, 
                                        'year_published': form.year_published.data, 'price': form.price.data , 'quantity': form.quantity.data,
                                        'summary': form.summary.data})
         flash('Product updated!', 'success')
         app.logger.info('Product Updated Sucessfully')
         return redirect(url_for('home'))
    else:
        app.logger.info('PRODUCT NOT UPDATED, ERROR')
    return render_template('create_product.html', title='Update', form=form, legend="Update Product")


@app.route("/product/<product_title>/delete", methods=['POST'])
@login_required
def delete_product(product_title):
    product =  products_collection.find_one({"title": product_title})
    products_collection.delete_one( products_collection.find_one({"title": product_title}) )
    flash('Product deleted', 'success')
    app.logger.info('Product Deleted Sucessfully')
    return redirect(url_for('home'))
