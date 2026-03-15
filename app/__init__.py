from flask import Flask
from .db import init_db
from .scheduler import start_scheduler

def create_app() -> Flask:
    app = Flask(__name__)

    from .routes import bp
    app.register_blueprint(bp)
    init_db()
    start_scheduler()
    return app
