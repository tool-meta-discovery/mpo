from L06Flask import *
from werkzeug.serving import WSGIRequestHandler
from flask import Flask
from flask_session import Session
from flask_cors import CORS
WSGIRequestHandler.protocol_version = "HTTP/1.1"


def create_app():
    app = Flask(__name__)
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    app.config["UPLOAD_FOLDER"] = ""
    app.register_blueprint(Configuration.bp, url_prefix="/configuration")
    app.register_blueprint(Import.bp, url_prefix="/import")
    app.register_blueprint(Event.bp, url_prefix="/event")
    app.register_blueprint(Trace.bp, url_prefix="/trace")
    app.register_blueprint(Algorithm.bp, url_prefix="/algorithm")
    app.register_blueprint(Quality.bp, url_prefix="/quality")
    app.register_blueprint(Optimization.bp, url_prefix="/optimizer")
    Session(app)
    CORS(app, supports_credentials=True)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
