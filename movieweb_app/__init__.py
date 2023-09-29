from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from movieweb_app.config import Config

bcrypt = Bcrypt()
db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions within the app context
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'users.signin'
    login_manager.login_message_category = 'info'

    from movieweb_app.blueprints.home import home_bp
    from movieweb_app.blueprints.movies import movies_bp
    from movieweb_app.blueprints.users import users_bp

    # Register blueprints
    app.register_blueprint(home_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(movies_bp)

    return app