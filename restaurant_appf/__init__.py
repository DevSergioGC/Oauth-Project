from email.policy import default
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'b4eff01d15e1f43fba89a616197522c7'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///restaurant.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['GOOGLE_CLIENT_ID'] = "957458512370-tdcmhj2hh18eci4dv99ftc6ej6liao11.apps.googleusercontent.com"
app.config['GOOGLE_CLIENT_SECRET'] = "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"
app.config['GITHUB_CLIENT_ID'] = "81d29af2d1b3967bd3e7"
app.config['GITHUB_CLIENT_SECRET'] = "ca511c18c03df0ca8f108e1c5c7a2776488e37f0"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from restaurant_appf import routes