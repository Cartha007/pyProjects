from blog import app
from blog.models import User
from flask import render_template, redirect, url_for, flash, request
from blog.models import User, Posts
from blog.forms import RegisterForm, LoginForm, PostForm, SearchForm
from blog import db
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/')
@app.route('/home')
def home():
    return render_template('coming.html')

@app.context_processor
def base():
    form = SearchForm
    return dict(form=form)

# Dashboard
@app.route('/dashboard')
@login_required
def dashboard_page():
    return render_template('dashboard.html')

@app.route('/posts')
def posts_page():
    # Get all the posts from the database
    posts = Posts.query.order_by(Posts.date_posted)
    return render_template('posts.html', posts=posts)

@app.route('/post/<int:id>')
def post_page(id):
    post = Posts.query.get_or_404(id)
    return render_template('post.html', post=post)

@app.route('/add-post', methods=['GET', 'POST'])
@login_required
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        poster = current_user.id
        post = Posts(title=form.title.data, content=form.content.data, poster_id=poster)
        form.title.data = ''
        form.content.data = ''
        
        # Add post data to database
        db.session.add(post)
        db.session.commit()
        
        # Return a message
        flash("Blog post submitted successfully!", category='success')
        
    # Redirect to the webpage
    return render_template("add_post.html", form=form)

# Registration, Login and logging out
@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)#This ensures that the user is logged in so that it prevents them from logging in again.
        flash(f"Account created succesfully! You are now logged in as {user_to_create.username}", category='success')
        return redirect(url_for('dashboard_page'))
    if form.errors != {}: #If there are errors from the validations
        for err_msg in form.errors.values():
            flash(f'{err_msg[0]}', category='danger')
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Succes! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('dashboard_page'))
        else:
            flash('Username and password do not match! Please try again.', category='danger')
            
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for('posts_page'))


# Error Pages

# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Internal Server Error
@app.errorhandler(500)
def server_error(e):
    return render_template('400.html'), 500