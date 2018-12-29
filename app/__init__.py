from flask import Flask, render_template
app = Flask (__name__)

from flask_babel import Babel, gettext
app.config.from_pyfile ('config.cfg')
babel = Babel (app)
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import models

from app import router