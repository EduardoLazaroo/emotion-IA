from flask import Flask
from app.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.secret_key = '3!4v#8x@1qL%z9pN^&*bD7uT$wA'

    from app.routes import main_bp
    app.register_blueprint(main_bp)

    return app
