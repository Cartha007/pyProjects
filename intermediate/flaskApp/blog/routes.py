from blog import app
from blog.models import User
from flask import render_template, redirect, url_for, flash, request
from blog.models import User, Posts
from blog.forms import RegisterForm, LoginForm, PostForm, SearchForm
from blog import db
from sqlalchemy import desc
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
import uuid as uuid
import os

@app.route('/')
@app.route('/home')
def home():
    return render_template('coming.html')

@app.context_processor
def base():
    form = SearchForm()
    return dict(form=form)

# Dashboard
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard_page():
    id = current_user.id
    form = RegisterForm()
    user_to_update = User.query.get_or_404(id)
    if request.method == "POST":
        user_to_update.username = request.form['username']
        user_to_update.email_address = request.form['email']
        user_to_update.about_author = request.form['about_author']
        
        # Check for profile picture
        if request.files['profile_pic']:
            user_to_update.profile_pic = request.files['profile_pic']
            
            # Grab the image name
            pic_filename = secure_filename(user_to_update.profile_pic.filename)
            
            # Set the UUID
            pic_name = str(uuid.uuid1()) + "_" + pic_filename
            # Save the image
            saver = request.files['profile_pic']
            
            # Saving the image as a string in the db
            user_to_update.profile_pic = pic_name
            try:
                saver.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name))
                db.session.commit()
                flash("User Updated Successfully!",category='success')
                return render_template('dashboard.html', form=form,
                                       user_to_update=user_to_update)
            except:
                flash("Error! Looks like there was a problem... try again!", category="warning")
                return render_template('dashboard.html', form=form,
                                       user_to_update=user_to_update)
        else:
            db.session.commit()
            flash("User Updated Successfully!", category='success')
            return render_template('dashboard.html', form = form,
                           user_to_update=user_to_update)
    else:
        return render_template('dashboard.html', form = form,
                        user_to_update=user_to_update, id = id)
    return render_template('dashboard.html')

# Update Database Record
@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update_user(id):
    form = RegisterForm()
    user_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        user_to_update.username = request.form['username']
        user_to_update.email_address = request.form['email']
        try:
            db.session.commit()
            flash("User Updated Successfully!", category='success')
            return render_template('update.html', form=form,
                                   user_to_update = user_to_update)
        except:
            flash("Error! Looks like there was a problem...try again!", category='warning')
            return render_template('update.html', form=form,
                                   user_to_update = user_to_update)
    else:
        return render_template('update.html', form=form,
                                   user_to_update = user_to_update, id = id)

@app.route('/delete/<int:id>')
@login_required
def delete_user(id):
    if id == current_user.id:
        user_to_delete = Users.query.get_or_404(id)
        form = RegisterForm()
        try:
            db.session.delete(user_to_delete)
            db.session.commit()
            flash("User Deleted Successfully!!")
            
            our_users = User.query.order_by(User.date_added)
            return render_template("register.html", form = form, our_users=our_users)
        except:
            flash("Whoops! There was a problem deleting user, try again...", category='warning')
            return render_template("register.html", form = form, our_users=our_users)
    else:
        flash("Sorry, you can't delete that user!", category='warning')
        return redirect(url_for('dashboard'))

@app.route('/posts')
def posts_page():
    # Get all the posts from the database and order in descending order
    posts = Posts.query.order_by(desc(Posts.date_posted))
    return render_template('posts.html', posts=posts)

@app.route('/post/<int:id>')
def post_page(id):
    post = Posts.query.get_or_404(id)
    return render_template('post.html', post=post)

# Create search function
@app.route('/search', methods=['POST'])
def search():
    form = SearchForm()
    posts = Posts.query
    if form.validate_on_submit():
        # Get data from submitted form
        searched = form.searched.data
        # Query the database
        posts = posts.filter(Posts.content.like('%' + searched + '%'))
        posts = posts.order_by(Posts.title).all()
        
        return render_template('search.html', form=form,
                               searched=searched,
                               posts=posts)

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

@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post = Posts.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        
        # Update Database
        db.session.add(post)
        db.session.commit()
        flash("Post Has Been Updated!")
        return redirect(url_for('post_page', id=post.id))
    if current_user.id == post.poster_id:
        form.title.data = post.title
        form.content.data = post.content
        return render_template('edit_post.html', form=form)
    else:
        flash("You aren't authorized to edit this post...")
        posts = Posts.query.order_by(Posts.date_posted)
        return render_template('posts.html', posts=posts)

@app.route('/posts/delete/<int:id>')
@login_required
def delete_post(id):
    post_to_delete = Posts.query.get_or_404(id)
    id = current_user.id
    if id == post_to_delete.poster.id:
        try:
            db.session.delete(post_to_delete)
            db.session.commit()
            
            # Return a message
            flash("Blog Post Was Deleted!", category='success')
            
            # Grab all the posts from the database
            posts = Posts.query.order_by(Posts.date_posted)
            return render_template('posts.html', posts=posts)
        except:
            # Return an error message
            flash("Whoops! There was a problem deleting post, try again...", category='danger')

            # Grab all the posts from the database
            posts = Posts.query.order_by(Posts.date_posted)
            return render_template('posts.html', posts=posts)
    else:
         # Return a message
            flash("You aren't authorized to delete that post!", category='warning')
            
            # Grab all the posts from the database
            posts = Posts.query.order_by(Posts.date_posted)
            return render_template('posts.html', posts=posts)

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