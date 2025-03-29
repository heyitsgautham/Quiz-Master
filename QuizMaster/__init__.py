from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

curr_dir = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(curr_dir, 'database', 'quizmaster.db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'secret_key'
app.config["UPLOAD_FOLDER"] = os.path.join(curr_dir, "static", "imgs")

db = SQLAlchemy()
db.init_app(app)

from . import models, controllers

with app.app_context():
    db.create_all()
    models.create_admin() 
