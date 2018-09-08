from flask import render_template, url_for, flash, redirect, request
from inventorymanagement import app, db, bcrypt
from inventorymanagement.forms import RegistrationForm, LoginForm, AddProduct, AddLocation, AddProductMovement
from inventorymanagement.models import User, Product, Location, ProductMovement
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title='Home')

@app.route("/about")
def about():
    return render_template('about.html', title="About")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your Account has been created', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout", methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('home'))

########################Products######################################

@app.route("/add_product", methods=['GET', 'POST'])
@login_required
def add_product():
    form = AddProduct()
    return render_template('add_product.html', title='Product', form=form)

@app.route("/edit_product")
@login_required
def edit_product():
    return render_template('edit_product.html', title='Product')

@app.route("/view_product")
@login_required
def view_product():
    return render_template('view_product.html', title='Product')

########################Locations######################################

@app.route("/add_location", methods=['GET', 'POST'])
@login_required
def add_location():
    form = AddLocation()
    return render_template('add_location.html', title='Location', form=form)

@app.route("/edit_location")
@login_required
def edit_location():
    return render_template('edit_location.html', title='Location')

@app.route("/view_location")
@login_required
def view_location():
    return render_template('view_location.html', title='Location') 

########################ProductMovements######################################

@app.route("/add_productmovement", methods=['GET', 'POST'])
@login_required
def add_productmovement():
    form = AddProductMovement()
    return render_template('add_productmovement.html', title='Movement', form=form)

@app.route("/edit_productmovement")
@login_required
def edit_productmovement():
    return render_template('edit_productmovement.html', title='Movement')


@app.route("/view_productmovement")
@login_required
def view_productmovement():
    return render_template('view_productmovement.html', title='Movement')

########################Sales######################################

@app.route("/view_sales")
@login_required
def view_sales():
    return render_template('view_sales.html', title='Sales')