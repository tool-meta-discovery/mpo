from flask import Blueprint
from flask_cors import CORS
from L01Import import *
from L06Flask.util import *
import json


bp = Blueprint("import", __name__)
CORS(bp, supports_credentials=True)


@bp.route("/get_available_data_models", methods=["POST"])
def get_available_data_models():
    required_request_content = ["celonis_key","celonis_url", "is_user_key"]
    session_content, request_content = prepare_request([],required_request_content)
    celonis_key, celonis_url, is_user_key = request_content
    if type(is_user_key) is str: is_user_key = (is_user_key.lower()=="true")
    connection = CelonisConnection(celonis_url, celonis_key, is_user_key)
    return json.dumps(connection.get_available_datamodels())


@bp.route("/import_data_model", methods=["POST"])
def import_data_model():
    requied_request_content = ["celonis_key","celonis_url", "is_user_key", "name"]
    session_content, request_content = prepare_request([], requied_request_content)
    celonis_key, celonis_url, is_user_key, name = request_content
    if type(is_user_key) is str: is_user_key = (is_user_key.lower()=="true")
    connection = CelonisConnection(celonis_url, celonis_key, is_user_key)
    session["content"][SessionKey.event_log_list].append(connection.get_DataSetObject(name))
    return "model has been imported"


@bp.route("/upload_local_file", methods=["POST"])
def upload_local_file():
    required_session_content = [SessionKey.upload_folder]
    required_request_content = ["separator", "file_type"]
    upload_folder, request_content = prepare_request(
        required_session_content, required_request_content)
    separator, file_type = request_content
    session["content"][SessionKey.plain_log], session["content"][SessionKey.log_name] = store_file(
        upload_folder, separator, file_type)
    return "file has been uploaded"


@bp.route("/get_column_names", methods=["GET"])
def get_column_names():
    plain_log, request_content = prepare_request([SessionKey.plain_log], [])
    return json.dumps(list(plain_log.columns.values))


@bp.route("/import_local_file", methods=["POST"])
def import_local_file():
    required_session_content = [
        SessionKey.upload_folder, SessionKey.plain_log, SessionKey.log_name]
    required_request_content = ["case", "time", "activity"]
    session_content, request_content = prepare_request(
        required_session_content, required_request_content)
    case, time, activity = request_content
    upload_folder, plain_log, name = session_content
    session["content"][SessionKey.event_log_list].append(
        DataExtraction.format_plain_log(plain_log, case, time, activity, name))
    return "local file has been imported"


@bp.route("/get_imported_data_sets", methods=["GET"])
def get_imported_data_sets():
    event_log_list, request_content = prepare_request(
        [SessionKey.event_log_list], [])
    result = [entry.get_info_dict() for entry in event_log_list]
    return json.dumps(result)


@bp.route("/select_data", methods=["POST"])
def select_data():
    event_log_list, log_name = prepare_request(
        [SessionKey.event_log_list], ["name"])
    event_log_list_dict = {entry.name: entry for entry in event_log_list}
    if not log_name in event_log_list_dict.keys():
        abort(418)
    session["content"][SessionKey.data_set_object] = event_log_list_dict[log_name]
    session["content"][SessionKey.pipeline_object] = PipelineObject()
    session["content"][SessionKey.pipeline_object].init_on_data_set(event_log_list_dict[log_name])
    return "data selected"


@bp.route("/delete_data", methods=["POST"])
def delete_data():
    event_log_list, log_name = prepare_request([SessionKey.event_log_list], ["name"])
    session["content"][SessionKey.event_log_list] = [log for log in event_log_list if log.name != log_name]
    return "data removed"

