from L06Flask.util import *
from flask_cors import CORS
from flask import Blueprint
import json



bp = Blueprint("event", __name__)
CORS(bp, supports_credentials=True)



@bp.route("/reset", methods=["POST"])
def reset_filter():
    pipe = get_pipe_line_object()
    pipe.reset_event_filter()
    return "event filter reset"



@bp.route("/get_parameter", methods=["GET"])
def get_parameter():
    pipe = get_pipe_line_object()
    return json.dumps(pipe.get_event_info_list())



@bp.route("/set_parameter", methods=["POST"])
def set_parameter():
    pipe = get_pipe_line_object()
    pipe.set_event_info_list(request.get_json())
    return "new info dict used"
