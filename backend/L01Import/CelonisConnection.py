from L03Discovery import DataSetObject
from pycelonis import get_celonis
import pm4py
import logging
from pm4py.objects.conversion.log import converter as log_converter


# establish connection to celonis when initiating this class
class CelonisConnection:

    # establishes connection to celonis
    # url of the celonis team
    # app token with permissions for at least: data integration- use & manage!
    # errors should be printed to stdout
    def __init__(self, celonis_url, token, is_user_key: bool = False):
        key_type = 'APP_KEY'
        if is_user_key:
            key_type = 'USER_KEY'

        logging.getLogger("pycelonis").setLevel(logging.ERROR)
        self.celonis = get_celonis(url=celonis_url, api_token=token, key_type=key_type)

    # returns names of available datamodels
    def get_available_datamodels(self):
        cel_datamodel_names = self.celonis.datamodels.data

        datamodels = []
        for model in cel_datamodel_names:
            datamodels.append(model.name)

        return datamodels

    # create DataSetObject from the selected Celonis datamodel
    def get_DataSetObject(self, datamodel_name):
        cel_datamodel = self.celonis.datamodels.find(datamodel_name)

        # always use first config for now
        cel_config = cel_datamodel.process_configurations[0]

        dataframe = cel_datamodel.tables.find(cel_config.activity_table.id).get_data_frame()
        dataframe_renamed = pm4py.format_dataframe(dataframe, case_id=cel_config.case_column,
                                                   activity_key=cel_config.activity_column,
                                                   timestamp_key=cel_config.timestamp_column)
        event_log = log_converter.apply(dataframe_renamed, variant=log_converter.Variants.TO_EVENT_LOG)

        return DataSetObject(dataframe=event_log, event_log=event_log, name=datamodel_name)