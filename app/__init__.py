from flask import Flask
from config import Config

from app.auth import auth_bp
from app.students import students_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(auth_bp)
    app.register_blueprint(students_bp)

    return app