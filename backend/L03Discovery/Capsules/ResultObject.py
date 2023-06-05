import os
import time
from typing import List, Tuple
import pandas as pd
import pickle
import io
from pathlib import Path
import uuid
from pm4py.visualization.petri_net import visualizer as pn_visualizer
import pm4py


class ResultObject:
    histories: List[pd.DataFrame]
    argmax: Tuple[int, int]
    finished: bool
    error: bool
    error_description: str

    def __init__(self, session_path):
        self.histories = list()
        self.argmax = (-1, -1)
        self.finished = False
        self.session_path = session_path
        self.error = False
        self.error_description = ""

    def get_info_dict(self):
        # todo sort and select top n histories
        # todo sort results histories
        # todo result human readable time format

        # todo stop process
        # todo feedback for completed
        if self.error:
            return {"error": self.error_description}

        histories = [hst for hst in self.histories if len(
            hst.columns) > 0 and hst["quality"].max() > 0]
        histories = sorted(histories,
                           key=lambda df: df["quality"].max(), reverse=True)
        histories = list(map(self.transform_history, histories))
        return {"histories": [entry.to_json(orient="records") for entry in histories][0:10], "finished": self.finished}

    def store_changes(self):
        if not os.path.exists(self.session_path):
            os.makedirs(self.session_path, exist_ok=True)
        with io.open(self.session_path + "/" + str(time.time()), "wb") as target:
            pickle.dump(self, target)

    def transform_model(self, pn, im, fm):
        visualization = pn_visualizer.apply(pn, im, fm)
        pn_model = visualization.source
        bpmn_model = pm4py.convert_to_bpmn(pn, im, fm)

        path = f"static/{self.session_path}"
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
        model_id = uuid.uuid4()
        pn_url = f"{path}/{model_id}.pnml"
        bpmn_url = f"{path}/{model_id}.bpmn"
        pm4py.write_pnml(pn, im, fm, pn_url)
        pm4py.write_bpmn(bpmn_model, bpmn_url)
        return pd.Series([pn_model, pn_url, bpmn_url], index=["model", "pnml_download_url", "bpmn_download_url"])

    def transform_history(self, history):
        transformed = history.copy()
        transformed.drop("quality", axis=1, inplace=True)
        transformed.rename(
            columns={"result": "model", "details": "quality"}, inplace=True)
        transformed[["model", "pnml_download_url", "bpmn_download_url"]] = transformed.model.apply(
            lambda res: self.transform_model(*res))
        parameter = [name for name in transformed.columns.values if name not in [
            "quality", "model", "pnml_download_url", "bpmn_download_url"]]
        transformed.reset_index(inplace=True)
        transformed["parameter"] = transformed[parameter].to_dict(
            orient="records")
        transformed.drop(parameter, axis=1, inplace=True)
        return transformed

    def set_error(self, description: str):
        self.error = True
        self.error_description = description
        self.store_changes()
