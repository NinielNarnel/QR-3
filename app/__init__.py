from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hola'

# CSRF protection
csrf = CSRFProtect(app)

# Configure the SQLite database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lab_inventory.db'
db = SQLAlchemy(app)

# Import your SQLAlchemy models here
from app import routes



