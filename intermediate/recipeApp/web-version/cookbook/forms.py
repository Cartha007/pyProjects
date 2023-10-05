from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from cookbook.models import User
# from flask_ckeditor import CKEditorField
from wtforms.widgets import TextArea
from flask_wtf.file import FileField


class RecipeForm(FlaskForm):
    recipe_name = StringField(label='Recipe Name', validators=[DataRequired()])
    recipe_desc = StringField(label='Description')
    recipe_ingredients = TextAreaField(label='Instructions', validators=[DataRequired()])
    recipe_instructions = TextAreaField(label='Instructions', validators=[DataRequired()])
    recipe_image = FileField(label="Recipe image")
    submit = SubmitField(label='Add Recipe')

class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username.')
        
    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email Address already exists! Please try a different email address.')

    username = StringField(label='Username:', validators=[Length(min=4, max=30), DataRequired()])
    email_address = StringField(label='Email:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1', message='Passwords must match'), DataRequired()])
    about_author = TextAreaField(label="About Author")
    profile_pic = FileField(label="Profile Pic")
    submit = SubmitField(label='Create Account')

class LoginForm(FlaskForm):
    username = StringField(label='Username:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Login')
    
class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    # content = StringField("Content", validators=[DataRequired()], widget=TextArea())
    # content = CKEditorField('Content', validators=[DataRequired()])
    # author = StringField("Author")
    submit = SubmitField("Submit")
    
class SearchForm(FlaskForm):
    searched = StringField("Searched", validators=[DataRequired()])
    submit = SubmitField("Submit")