from cookbook import db, login_manager
from cookbook import bcrypt
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

user_recipe = db.Table('user_recipe',
                       db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                       db.Column('recipe_id', db.Integer, db.ForeignKey('recipes.recipe_id')),
                       db.Column('saved_at', db.DateTime, default=datetime.utcnow))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)
    date_updated = db.Column(db.DateTime)
    profile_pic = db.Column(db.String(), nullable=True)
    # User can create many recipes (One to many relationship)
    recipes = db.relationship('Recipes', backref='creator')
    # Many to many relationship
    saved_recipes = db.relationship('Recipes', secondary=user_recipe, backref='saved_by')
    
    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute!')
        # return self.password
    
    # Encrypts the password in the db
    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')
        
    # Verify the Password
    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)
    
    def __repr__(self):
        return f'<Username: {self.username}'
    
class Recipes(db.Model):
    recipe_id = db.Column(db.Integer(), primary_key=True)
    recipe_created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipe_name = db.Column(db.String(length=30), nullable=False)
    recipe_desc = db.Column(db.String(length=100), nullable=True)
    recipe_ingredients = db.Column(db.Text(), nullable=False)
    recipe_instructions = db.Column(db.Text(), nullable=False)
    recipe_category = db.Column(db.Text(), nullable=True)
    recipe_ratings =db.Column(db.Integer())
    # recipe_reviews =
    recipe_image = db.Column(db.String(), nullable=True)
    recipe_created_at = db.Column(db.DateTime, default=datetime.utcnow)
    recipe_updated_at = db.Column(db.DateTime)