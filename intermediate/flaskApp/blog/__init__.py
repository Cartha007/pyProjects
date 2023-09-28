from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_ckeditor import CKEditor

app = Flask(__name__)
# App configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SECRET_KEY'] = 'secret_key'
# Database
db = SQLAlchemy(app)
migrate = Migrate(app, db)
#  For Encryption
bcrypt = Bcrypt(app)
# Add CKEditor
ckeditor = CKEditor(app)
# Login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"
# For file upload
UPLOAD_FOLDER = 'blog/static/images/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from blog import routes