from flask import Flask
from config import Config
from extensions import db, ma
from flask_migrate import Migrate

# import models (VERY IMPORTANT)
from models import *

# import blueprints
from routes.auth import auth_bp
from routes.lessons import lessons_bp
from routes.questions import questions_bp
from routes.progress import progress_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # initialize extensions
    db.init_app(app)
    ma.init_app(app)
    migrate = Migrate(app, db)

    # register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(lessons_bp)
    app.register_blueprint(questions_bp)
    app.register_blueprint(progress_bp)

    return app