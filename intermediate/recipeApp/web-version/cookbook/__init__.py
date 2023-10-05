from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

# App configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SECRET_KEY'] = 'secret_key'

# Database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#  For Encryption
bcrypt = Bcrypt(app)

# Login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"

# For file upload
RECIPE_UPLOAD_FOLDER = 'blog/static/images/recipe_imgs'
app.config['RECIPE_IMAGE_UPLOAD_FOLDER'] = RECIPE_UPLOAD_FOLDER

PROFILE_UPLOAD_FOLDER = 'blog/static/images/profile_imgs'
app.config['PROFILE_PIC_UPLOAD_FOLDER'] = PROFILE_UPLOAD_FOLDER

from cookbook import routes