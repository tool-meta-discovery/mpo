from L06Flask.util import *
from flask_cors import CORS
from flask import Blueprint
import json



bp = Blueprint("algorithm", __name__)
CORS(bp, supports_credentials=True)



@bp.route("/reset", methods=["POST"])
def reset_algorithm():
    pipe = get_pipe_line_object()
    pipe.reset_algorithm()
    return "trace algorithm reset"



@bp.route("/get_parameter", methods=["GET"])
def get_parameter():
    pipe = get_pipe_line_object()
    return json.dumps(pipe.get_algo_info_list())



@bp.route("/set_parameter", methods=["POST"])
def set_parameter():
    pipe = get_pipe_line_object()
    pipe.set_algo_info_list(request.get_json())
    return "new info dict used"
