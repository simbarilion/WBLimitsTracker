from flask import Flask
from .db import init_db
from .routes import bp
from .scheduler import start_scheduler

def create_app():
    app = Flask(__name__)
    app.register_blueprint(bp)
    init_db()
    start_scheduler()
    return app
