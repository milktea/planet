from flask import Flask
from planet.config import Config
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

import planet.models
import planet.api
import planet.seed

db.create_all()
