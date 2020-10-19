from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import Config, ProductionConfig, DevelopmentConfig

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import User, Song, Comments

from routes.user_route import *
from routes.song_route import *
from routes.comment_route import *

@app.route("/")
def index():
    return render_template("Home.html")
