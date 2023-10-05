from cookbook import app
from cookbook.models import User, Recipes
from flask import render_template, redirect, url_for, flash, request
from cookbook.forms import RegisterForm, LoginForm, SearchForm, RecipeForm
from cookbook import db
from sqlalchemy import desc
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.context_processor
def base():
    form = SearchForm()
    return dict(form=form)

@app.route('/add-recipe', methods=['GET', 'POST'])
@login_required
def add_recipe():
    form = RecipeForm()
    if form.validate_on_submit():
        poster = current_user.id
        
        # Handle file upload (assuming you're storing the image on the server)
        if form.recipe_image.data:
            image_filename = secure_filename(form.recipe_image.data.filename)
            # Set the UUID
            image_name = str(uuid.uuid1()) + "_" + image_filename
            # Store the image
            saver = form.recipe_image.data
            try:
                image_path = os.path.join(app.config['RECIPE_IMAGE_UPLOAD_FOLDER'], image_name)
                saver.save(image_path)
            except:
                flash("Error! Looks like there was a problem... try again!", category="warning")
                return render_template('add_recipe.html', form=form)
        
        recipe = Recipes(
            recipe_name=form.recipe_name.data,
            recipe_desc=form.recipe_desc.data,
            recipe_ingredients=form.recipe_ingredients.data,
            recipe_instructions=form.recipe_instructions.data,
            recipe_image=image_name if form.recipe_image.data else None,
            recipe_created_by=current_user.id
        )
        
        # Add the new recipe to the database
        db.session.add(recipe)
        db.session.commit()
        
        # Return a message
        flash("Recipe added successfully!", category='success')
        return redirect(url_for('home_page', recipe_id=recipe.recipe_id))
        
    # Redirect to the webpage
    return render_template("add_recipe.html", form=form)

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
        return redirect(url_for('home_page'))
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
            return redirect(url_for('home_page'))
        else:
            flash('Username and password do not match! Please try again.', category='danger')
            
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for('home_page'))


# Error Pages

# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Internal Server Error
@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500