from L04Optimization.Optimizer import *
from L03Discovery.Capsules.ResultObject import *
from L06Flask.util import *
from flask_cors import CORS
from flask import Blueprint
import os
from pathlib import Path
import pickle
import io
import json


bp = Blueprint("optimizer", __name__)
CORS(bp, supports_credentials=True)


@bp.route("/set_timeout", methods=["POST"])
def set_time_out():
    session_content, time_out = prepare_request([], ["seconds"])
    session["content"][SessionKey.optimizer_timeout] = time_out if isinstance(time_out, int) else abort(418)
    return "time out set"


@bp.route("/get_all_optimizer", methods=["GET"])
def get_all_optimizer():
    return json.dumps([entry.name for entry in AvailableAlgorithms])


@bp.route("/set_optimizer", methods=["POST"])
def set_optimizer():
    session_content, kernel = prepare_request([], ["kernel"])
    session["content"][SessionKey.optimizer_kernel] = AvailableAlgorithms.__getitem__(
        kernel)
    return "kernel set"


@bp.route("/run_optimizer", methods=["GET"])
def run_optimizer():
    session_content, request_content, = prepare_request(
        [SessionKey.internal_folder, SessionKey.result_folder,SessionKey.pipeline_object,SessionKey.data_set_object], [])
    internal_folder, result_folder, pipe, data = session_content
    with io.open(internal_folder + "/content.pickle", "wb") as pickle_file:
        pickle.dump(session["content"], pickle_file)
    with io.open(result_folder + "/"+str(time.time()), "wb") as pickle_file:
        pickle.dump(ResultObject(""), pickle_file)
    return "optimizer is running"


@bp.route("/get_result", methods=["GET"])
def store_result():
    result_folder, request_content = prepare_request(
        [SessionKey.result_folder], [])
    file_path = max(Path(result_folder).glob("*"), key=os.path.getmtime)
    with io.open(file_path, "rb") as pickle_file:
        result_object = pickle.load(pickle_file)
    return result_object.get_info_dict()


@bp.route("/stop_optimizer", methods=["GET"])
def stop_optimizer():
    session["content"].create_sub_folder("abort")
    return "optimizer aborted"
