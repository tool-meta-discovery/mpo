from L03Discovery import DataSetObject
from pm4py.objects.log.util import dataframe_utils
from pm4py.objects.conversion.log import converter as log_converter
import pm4py
import pandas as pd


class DataExtraction:

    def extract_csv(self, file_path, case_column, activity_column, time_column, separator: str = ';'):
        log_csv = pd.read_csv(file_path, sep=separator)
        log_csv = dataframe_utils.convert_timestamp_columns_in_df(log_csv)
        log_csv.rename(columns={case_column: 'case:concept',
                       activity_column: 'concept:name', time_column: 'time:timestamp'}, inplace=True)
        log_csv = log_csv.sort_values(time_column)
        return DataSetObject(log_csv)

    def extract_xes(self, file_path):
        log = pm4py.read_xes(file_path)
        return DataSetObject(event_log=log)

    @staticmethod
    def format_plain_log(log, case, time, activity, name):
        log = dataframe_utils.convert_timestamp_columns_in_df(log)
        log = log.sort_values(time)
        log.rename(columns={activity: "concept:name",
                   time: "time:timestamp"}, inplace=True)
        parameters = {
            log_converter.Variants.TO_EVENT_LOG.value.Parameters.CASE_ID_KEY: case}
        return DataSetObject(log_converter.apply(log, parameters=parameters), name=name)
