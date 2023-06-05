from flask_cors import CORS
from flask import Blueprint
from L06Flask.util import *



bp = Blueprint("configuration", __name__)
CORS(bp, supports_credentials=True)



@bp.route("/start_session", methods=["GET"])
def start_session():
    session["content"] = SessionObject()
    return "check your cookies"


