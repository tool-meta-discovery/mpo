from flask import request, session, abort
from enum import Enum
import bson
import os
from L03Discovery import PipelineObject
import pandas as pd
import pm4py


class SessionKey(Enum):

    celonis_url = 0
    celonis_key = 1
    is_user_key = 2
    upload_folder = 3
    internal_folder = 4
    result_folder = 5
    pipeline_object = 6
    data_set_object = 7
    optimizer_kernel = 8
    optimizer_timeout = 9
    identifier = 10
    event_log_list = 11
    plain_log = 12
    log_name = 14
    abort_folder = 15


class SessionObject:

    def __init__(self):

        self.data = {}
        self.base_folder = "flask_storage_folder"
        self.setup_base_folder()
        self.__setitem__(SessionKey.event_log_list, [])
        self.__setitem__(SessionKey.identifier, bson.ObjectId())
        self.__setitem__(SessionKey.pipeline_object, PipelineObject())
        self.__setitem__(SessionKey.upload_folder,
                         self.create_sub_folder("upload"))
        self.__setitem__(SessionKey.internal_folder,
                         self.create_sub_folder("internal"))
        self.__setitem__(SessionKey.result_folder,
                         self.create_sub_folder("result"))

    def setup_base_folder(self):
        if not os.path.isdir(self.base_folder):
            os.makedirs(self.base_folder)
        if not os.path.isdir(self.base_folder+"/upload"):
            os.makedirs(self.base_folder+"/upload")
        if not os.path.isdir(self.base_folder+"/result"):
            os.makedirs(self.base_folder+"/result")
        if not os.path.isdir(self.base_folder+"/internal"):
            os.makedirs(self.base_folder+"/internal")

    def create_sub_folder(self, name):
        sub_folder = self.base_folder + "/"+name + \
            "/" + str(self[SessionKey.identifier])
        if not os.path.isdir(sub_folder):
            os.makedirs(sub_folder)
        return sub_folder

    def __getitem__(self, item):
        return self.data[item] if item in self.data else abort(418)

    def __setitem__(self, key, value):
        return self.data.__setitem__(key, value) if isinstance(key, SessionKey) else abort(418)


def abort_if_invalid_session():
    if not "content" in session or not isinstance(session["content"], SessionObject):
        abort(401)


def abort_if_missing_content(required_content_list):
    return tuple([session["content"][required_content] for required_content in required_content_list])


def get_submission_data():
    try:
        data = request.get_json()
        return data if data else request.form
    except:
        return request.form


def abort_if_missing_submission(required_submission_list):
    submission_content = get_submission_data()
    if not all([required_submission in submission_content for required_submission in required_submission_list]):
        abort(418)
    return tuple([submission_content[required_submission] for required_submission in required_submission_list])


def prepare_request(required_content_list, required_submission_list):
    abort_if_invalid_session()
    content = abort_if_missing_content(required_content_list)
    submission = abort_if_missing_submission(required_submission_list)
    if len(content) == 1:
        content = content[0]
    if len(submission) == 1:
        submission = submission[0]
    return content, submission


def store_file(upload_folder, separator, file_type):
    upload_file = request.files["file"]
    file_path = upload_folder+"/"+upload_file.filename
    upload_file.save(file_path)
    if file_type == "csv":
        log = pd.read_csv(file_path, sep=separator)
    if file_type == "xes":
        log = pm4py.convert_to_dataframe(pm4py.read_xes(file_path))
    return (log, upload_file.filename) if file_type in ["csv", "xes"] else (None, None)


def get_pipe_line_object():
    pipe_line_object, request_content = prepare_request(
        [SessionKey.pipeline_object], [])
    return pipe_line_object
