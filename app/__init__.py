from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager 
from flask_mail import Mail
from flask import Blueprint
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SECRET_KEY'] = 'hola'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lab_inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# CSRF protection
csrf = CSRFProtect(app)

# Configure the SQLite database URI
db = SQLAlchemy(app)
auth= Blueprint ('auth',__name__) 
migrate = Migrate(app, db)

# Import your SQLAlchemy models here
from app import routes


login_manager = LoginManager(app)
login_manager.login_view = 'login'

