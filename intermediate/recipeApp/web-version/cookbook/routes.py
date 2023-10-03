from cookbook import app
from cookbook.models import User, Recipes
from flask import render_template, redirect, url_for, flash, request
# from cookbook.forms import RegisterForm, LoginForm, SearchForm
from cookbook import db
from sqlalchemy import desc
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.context_processor
def base():
    form = None
    return dict(form=form)

# Error Pages

# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Internal Server Error
@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500