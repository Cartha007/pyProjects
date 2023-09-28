from blog import app
from blog.models import User
from flask import render_template, redirect, url_for, flash, request
from blog.forms import RegisterForm, LoginForm
from blog import db
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/')
@app.route('/home')
def home():
    return render_template('coming.html')

# Login, Registration and logging out
@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm
    return render_template('login.html', form=form)

@app.route('/logut')
@login_required
def logout():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    pass


# Error Pages

# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Internal Server Error
@app.errorhandler(500)
def server_error(e):
    return render_template('400.html'), 500