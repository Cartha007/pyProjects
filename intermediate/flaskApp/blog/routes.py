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
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Succes! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('dashboard'))
        else:
            flash('Username and password do not match! Please try again.', category='danger')
            
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for('home'))

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