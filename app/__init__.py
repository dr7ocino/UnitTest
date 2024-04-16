from flask import Flask
from .events import socketio
from .routes import main
from .controllers.operaciones_conductor import *

def createApp():
    app = Flask(__name__)
    app.config['DEBUG'] = True
    app.config['SECRET_KEY'] = "secret"
    app.register_blueprint(main)
    socketio.init_app(app)
    return app