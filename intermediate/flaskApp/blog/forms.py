from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

class NamerForm(FlaskForm):
    name = StringField(label="What's Your Name", validators=[DataRequired()])
    submit = SubmitField("Submit")