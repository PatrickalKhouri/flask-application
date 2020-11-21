from flask import Flask, render_template, url_for
from forms import RegistrationForm, LoginForm
app = Flask(__name__)

app.config['SECRET_KEY'] = '23b8868cf282837c556e88fd2c41cb'

products = [
    {
       'reference': 'NK 212',
       'country': 'India',
       'type':'kilim',
       'height': 2,
       'width': 1.5,
       'm2': 3,
       'quantity': 5,
       'price': 1000,
       'description': 'Kilim Indian - Red',
       'Images': "...",
       'created_at':'November 20, 2019'
    },
    {
       'reference': 'HZ 0156',
       'country': 'Afganistan',
       'type':'carpet',
       'height': 5,
       'width': 4,
       'm2': 20,
       'quantity': 3,
       'price': 12000,
       'description': 'Large colorfull carpet',
       'Images': "...",
       'created_at':'November 10, 2019'
    }
]

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
        flash(f'Account created for {form.username.data}!', 'success')
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