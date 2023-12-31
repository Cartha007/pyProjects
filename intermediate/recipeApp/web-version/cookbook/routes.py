# On Hold
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

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def dashboard():
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

@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update_user_info(id):
    form = RegisterForm()
    user_to_update = Users.query.get_or_404(id)
    if request.method == 'POST':
        user_to_update.username = request.form['username']
        user_to_update.email_address = request.form['email']
        try:
            db.session.commit()
            flash("User Updated Successfully!", category='success')
            return render_template('update_user.html', form=form, user_to_update=user_to_update)
        except:
            flash("Error! Looks like there was a problem... Try again!", category='warning')
            return render_template('update_user.html', form=form, user_to_update=user_to_update)
    else:
        return render_template('update.html', form=form, user_to_update = user_to_update, id = id)
    
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

@app.route('/recipes')
def view_recipes():
    # Get all the recipes from the database and order in descending order
    recipes = Recipes.query.order_by(desc(Recipes.recipe_created_at))
    return render_template('recipes.html', recipes=recipes)

@app.route('/recipe/<int:id>')
def view_recipe(id):
    recipe = Recipes.query.get_or_404(id)
    return render_template('recipe.html', recipe=recipe)

# Search function
@app.route('/search', methods=['POST'])
def search():
    form = SearchForm()
    recipes = Recipes.query
    if form.validate_on_submit():
        # Get data from submitted form
        searched = form.searched.data
        # Query the database
        recipes = recipes.filter(Recipes.recipe_name.like('%' + searched + '%'))
        recipes = recipes.order_by(Recipes.recipe_name).all()
        
        return render_template('search.html', form=form,
                               searched=searched,
                               recipes=recipes)

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

@app.route('/recipes/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_recipe(id):
    recipe = Recipes.query.get_or_404(id)
    form = RecipeForm()

    if current_user.id == recipe.recipe_created_by:
        if form.validate_on_submit():
            recipe.recipe_name = form.recipe_name.data
            recipe.recipe_desc = form.recipe_desc.data
            recipe.recipe_ingredients = form.recipe_ingredients.data
            recipe.recipe_instructions = form.recipe_instructions.data

            db.session.commit()
            flash("Recipe Has Been Updated!", category='success')
            return redirect(url_for('view_recipe', id=recipe.recipe_id))

        # Populate the form fields with the recipe data
        form.recipe_name.data = recipe.recipe_name
        form.recipe_desc.data = recipe.recipe_desc
        form.recipe_ingredients.data = recipe.recipe_ingredients
        form.recipe_instructions.data = recipe.recipe_instructions

        return render_template('edit_recipe.html', form=form, recipe=recipe)
    else:
        flash("You aren't authorized to edit this recipe!!", category='warning')
        recipes = Recipes.query.order_by(Recipes.recipe_created_at)
        return render_template('recipes.html', recipes=recipes)


@app.route('/recipes/delete/<int:id>')
@login_required
def delete_recipe(id):
    recipe_to_delete = Recipes.query.get_or_404(id)
    id = current_user.id
    if id == recipe_to_delete.recipe_created_by:
        try:
            db.session.delete(recipe_to_delete)
            db.session.commit()
            
            flash("Recipe has been deleted!", category="success")
            
            recipes = Recipes.query.order_by(Recipes.recipe_created_at)
            return render_template('recipes.html', recipes=recipes)
        except:
            flash("Whoops! There was a problem deleting the recipe, try again..", category="danger")
            
            recipes = Recipes.query.order_by(Recipes.recipe_created_at)
            return render_template('recipes.html', recipes=recipes)
    else:
        flash("You aren't authorized to delete that recipe!", category='warning')
        
        recipes = Recipes.query.order_by(Recipes.recipe_created_at)
        return render_template('recipes.html', recipes=recipes)


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