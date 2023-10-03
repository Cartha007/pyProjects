from cookbook import app
from cookbook.models import Users, Recipes
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