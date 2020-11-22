from flask import Flask, render_template, url_for, flash, redirect  
from forms import RegistrationForm, LoginForm, ProductForm
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, current_user, logout_user, login_required

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
products = []

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

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8)')
        users_collection.insert_one({'username': form.username.data, 'email': form.email.data, 'password': hashed_password, 'admin': False })
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = users_collection.find_one({"email": form.email.data})
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
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
         return redirect(url_for('home'))
    return render_template('create_product.html', title='New Product', form=form, legend="Update Product")

@app.route("/product/<product_title>")
def product(product_title):
    product =  products_collection.find_one({"title": product_title})
    return render_template('product.html', title=product["title"], product=product)

@app.route("/product/<product_title>/update", methods=['GET', 'POST'])
def update_product(product_title):
    product =  products_collection.find_one({"title": product_title})
    form = ProductForm()
    if form.validate_on_submit():
         products_collection.update( products_collection.find_one({"title": product_title}), {'title': form.title.data, 'author': form.author.data, 'editor': form.editor.data, 
                                        'year_published': form.year_published.data, 'price': form.price.data , 'quantity': form.quantity.data,
                                        'summary': form.summary.data})
         flash('Product updated!', 'success')
         return redirect(url_for('home'))
    return render_template('create_product.html', title='Update', form=form, legend="Update Product")


@app.route("/product/<product_title>/delete", methods=['POST'])
def delete_product(product_title):
    product =  products_collection.find_one({"title": product_title})
    products_collection.delete_one( products_collection.find_one({"title": product_title}) )
    flash('Product deleted', 'success')
    return redirect(url_for('home'))

