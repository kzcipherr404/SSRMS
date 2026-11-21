from flask import Flask
from config import Config
from app.auth import auth_bp


def create_app():
    """
    Create and configure the Flask application.
    """

    app = Flask(__name__)

    app.config.from_object(Config)

    # Register authentication routes
    app.register_blueprint(auth_bp)

    return app