from base64 import decode
from flask import Flask, render_template,url_for,request,redirect,Response,session,send_file,flash
from app.forms import RegistrationForm,LoginForm,UpdateAccountForm
from flask_sqlalchemy import SQLAlchemy
from app.models import *
from app import app,db,bcrypt
from flask_login import login_user,current_user,logout_user,login_required

@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        if request.form.get('Log') == 'Log in':
            return redirect(url_for('login'))
        elif request.form.get('Sign') == 'Sign in':
            return redirect(url_for('register'))
        elif request.form.get('Products') == 'Products':
            return redirect(url_for('products'))
    elif request.method == 'GET':
        return render_template('index.html')

@app.route("/about")
def about():
    return render_template('error.html', title = "Ekran")

@app.route("/products")
def products():
    return render_template('products.html',title = "Products")

@app.route("/register",methods = ['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data
       ,email = form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account have been created, you can log in!','success')
        return redirect(url_for('login'))
    return render_template('register.html',title = "Register",form = form)

@app.route("/login",methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember = form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login unsucesfull. Please check your username and password','danger')
    return render_template('login.html',title ="Login",form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/cart",methods=['GET', 'POST'])
@login_required
def cart():
    return render_template('cart.html',title = "Cart")

@app.route("/account",methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.first_name = form.first_name.data
        current_user.second_name = form.second_name.data
        current_user.phone = form.phone.data
        db.session.commit()
        flash('Your account has been updated','success')
        return redirect(url_for('account'))
    elif request.method == "GET":
        form.username.data =  current_user.username
        form.email.data =  current_user.email
        form.first_name.data =  current_user.first_name
        form.second_name.data =  current_user.second_name
        form.phone.data =  current_user.phone
        
    return render_template('account.html',title ="Account",form = form)

