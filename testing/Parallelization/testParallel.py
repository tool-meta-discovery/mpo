import matplotlib.pyplot

from L03Discovery import ResultObject
from L03Discovery.Capsules.PipelineObject import PipelineObject
from L03Discovery.Capsules.DataSetObject import DataSetObject
from L02Parameter.Enumeration.ParameterType import ParameterType
import datetime

from L05Parallelization.ParallelProcessor import ParallelProcessor

# we need to ensure that parallel processing is always started from main thread because problems
if __name__ == '__main__':

    """Load a test data set"""
    import pandas as pd
    from pm4py.objects.log.util import dataframe_utils
    from pm4py.objects.conversion.log import converter as log_converter

    log_csv = pd.read_csv('data/BPI2016_Complaints.csv', sep=';')
    log_csv = dataframe_utils.convert_timestamp_columns_in_df(log_csv)
    log_csv = log_csv.sort_values('ContactDate')
    log_csv.rename(columns={'ComplaintTopic_EN': 'concept:name', 'ContactDate': 'time:timestamp'}, inplace=True)
    parameters = {log_converter.Variants.TO_EVENT_LOG.value.Parameters.CASE_ID_KEY: 'CustomerID'}
    log = log_converter.apply(log_csv, parameters=parameters)
    capsule_object = DataSetObject(log)


    """ Setup the pipeline object first, it will guide you through the 
    full process of specifying everything needed for the optimization. """
    pipeLineObject = PipelineObject()

    available_filters_dict = pipeLineObject.get_available_event_filter()
    for identifier in available_filters_dict.keys():
        print("Supported Filter Identifier: ", identifier)

    exclude_filter_list = []
    pipeLineObject.unselect_event_filter(exclude_filter_list)
    print("Excluded The Following Filter Identifier: ", exclude_filter_list)

    for getAllStepObjects in [pipeLineObject.get_selected_event_filter, pipeLineObject.get_selected_trace_filter]:
        selected_objects = getAllStepObjects()
        for identifier in selected_objects.keys():
            print("Setting Up Parameter For Filter Identifier: ", identifier)

            filter = selected_objects[identifier]
            available_parameter_names = filter.get_all_parameter_names()
            print("The Following Parameters Are Available: ", available_parameter_names)

            for parameter_name in available_parameter_names:
                print("Setting Up Parameter With The Name: ", parameter_name)

                parameter = filter.get_one_parameter(parameter_name)
                print(parameter.description)
                print(parameter.value_type)

                if parameter.value_type == ParameterType.Time:
                    parameter.set_current_value(datetime.datetime.utcfromtimestamp(datetime.datetime.fromisoformat("2015-07-03T00:00").timestamp()))
                    parameter.set_upper_range(datetime.datetime.utcfromtimestamp(datetime.datetime.fromisoformat("2016-02-28T23:59").timestamp()))
                    parameter.set_lower_range(datetime.datetime.utcfromtimestamp(datetime.datetime.fromisoformat("2015-07-03T00:00").timestamp()))

                if parameter.value_type == ParameterType.Numeric:
                    parameter.set_current_value(3475.321)
                    parameter.set_lower_range(-58798.346)
                    parameter.set_upper_range(987348.365)

                if parameter.value_type == ParameterType.Integral:
                    parameter.set_current_value(3445)
                    parameter.set_lower_range(-34535)
                    parameter.set_upper_range(763553)

                if parameter.value_type == ParameterType.Selection:
                    available_option_set = parameter.get_selection_set()
                    restricted_option_set = available_option_set[:-1]
                    parameter.set_selection_set(restricted_option_set)

                if parameter.value_type == ParameterType.FixedValue:
                    pass

    from L03Discovery.Enumeration.QualityMeasureType import QualityMeasureType
    available_quality_measures = pipeLineObject.get_available_quality_measure()
    # since we only have one measure anyway at the moment, we do not need to remove any
    pipeLineObject.unselect_quality_measure([QualityMeasureType.PrecisionAlignment,
                                             QualityMeasureType.ReplayFitnessAlignment,
                                             QualityMeasureType.GeneralizationToken,
                                             QualityMeasureType.SimplicityArcDegree])

    """create a parallel processor"""
    result = ResultObject()
    processor = ParallelProcessor()

    processor.with_quality_threshold(0.99).with_data(capsule_object).with_pipeline(pipeLineObject)\
        .with_max_time(datetime.timedelta(seconds=60)).with_result_object(result)
    print("===Staring Prallel Processing===")
    processor.execute_optimization_parallel()
    print("===Parallel Processing Complete===\nResult:\n")
    df, hist = result.get_info_dict()["top_frame"], result.get_info_dict()["top_history"]
    print(df)
    """plot the history of scores for the best result, to see if optimizer does anything"""
    hist.reset_index().drop(columns=["index"])["quality"].plot()
    matplotlib.pyplot.show()

