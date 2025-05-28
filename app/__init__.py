from flask import Flask
from config import Config
from extensions import db, jwt

from routes.auth import auth_bp
from routes.plans import plans_bp
from routes.timer import timer_bp
from routes.dashboard import dashboard_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(plans_bp, url_prefix="/api")
    app.register_blueprint(timer_bp, url_prefix="/api")
    app.register_blueprint(dashboard_bp, url_prefix="/api")

    return app

