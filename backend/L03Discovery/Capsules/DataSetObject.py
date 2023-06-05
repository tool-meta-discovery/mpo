from pm4py.objects.conversion.log import converter as log_converter
from pm4py.objects.log.obj import EventLog
import pandas as pd
import datetime


class DataSetObject:

    def __init__(self, dataframe: pd.DataFrame = None, event_log: EventLog = None, name=None):
        self.dataframe = dataframe
        self.original_data = dataframe
        self.cases = len(self.original_data)
        self.events = sum([len(entry) for entry in self.original_data], 0)
        self.date = datetime.datetime.now()
        self.name = name
        self.event_log = event_log
        self.bpmn = None
        self.process_tree = None
        self.result = None
        self.score = None
        self.score_dict = None
        if isinstance(self.dataframe, pd.DataFrame):
            self.head = self.dataframe.head(100)
        else:
            self.head = log_converter.apply(
                self.dataframe, variant=log_converter.TO_DATA_FRAME).head(100)

    def get_info_dict(self):
        return {"name": self.name, "cases": self.cases, "events": self.events, "date": str(self.date), "head": self.head.to_json(orient='records')}
