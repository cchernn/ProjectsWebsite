import os
import logging
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_dynamo import Dynamo
from flask_mail import Mail
from logging.handlers import SMTPHandler
from config import Config

login=LoginManager()
login.login_view = "auth.login"
login.login_message = "Please sign in to access this page."
dynamo = Dynamo()
bootstrap=Bootstrap()
mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    login.init_app(app)
    dynamo.init_app(app)
    bootstrap.init_app(app)
    mail.init_app(app)

    with app.app_context():
        dynamo.create_all(wait=True)

        from app.main import bp as main_bp
        app.register_blueprint(main_bp)

        from app.auth import bp as auth_bp
        app.register_blueprint(auth_bp)

        from app.errors import bp as errors_bp
        app.register_blueprint(errors_bp)

        from app import models # remove if redundant

        return app

