
from L03Discovery import *


""" Setup the pipeline object first, it will guide you through the 
full process of specifying everything needed for the optimization. """
pipeLineObject = PipelineObject()



""" The pipeline object already contains sub objects for all the 
available filters. To check which ones are available,use the 
get_available_event_filter method. The return value will be a 
dictionary with the filter name (enum) as key and the filter 
object as value. Use the name (enum) to identify the filter. """

available_filters_dict = pipeLineObject.get_available_event_filter()
for identifier in available_filters_dict.keys():
	print("Supported Filter Identifier: ",identifier)



""" First we have to select which filter will be regarded during 
the optimization process. The default behaviour is to use all 
available filters. This means you have to actively UN-select all 
the filter you do NOT want to use. For identification, use the 
identifiers provided as dictionary keys above. In this case we 
do not remove any filter, since there is only one supported yet."""

exclude_filter_list = []
pipeLineObject.unselect_event_filter(exclude_filter_list)
print("Excluded The Following Filter Identifier: ",exclude_filter_list)


""" You can do the exact same thing for the trace filtering techniques
and the algorithm selection. Right now, we  simply leave everything
on the default configurations. This means that all available trace filters
and discovery algorithms will be used. Optimizing along multiple quality
measures at the same time is not possible, so keep in mind to only select 
one quality measure as soon as mutliple are available. """

available_quality_measures = pipeLineObject.get_available_quality_measure()
#since we only have one measure anyway at the moment, we do not need to remove any
pipeLineObject.unselect_quality_measure([])



""" Now the pipe line setup is completed and we can proceed with the
optimization. For this purpose you can ask the pipeline for the list of
resulting optimization objects. These objects are made such that they 
each represent one unique combination of the filters and algorithms that
the user allowed for the optimization process. Within each single one of 
these objects the optimizer need to find the best parameter combination. 
In the end the local optima of the different objects can be compared to 
determine which filter and algorithm delivers the best result. Please 
note that each object is fully independent of all the other objects. The
optimization for them can therefore be done in parallel. In this case
there will only be one such object, since we only have one filter and 
one algorithm implemented yet. """

resulting_optimization_objects = pipeLineObject.get_optimization_objects()
example_object = resulting_optimization_objects[0]



""""We need to find values for the following parameters with the optimizer
If you want to try out one combination of values, set them in each of the 
parameter and execute the object on the dataset at hand. Remember that you
do not need to modify FixedValues Parameters. These are the same objects 
as described in the setup example above, so you can access their type/etc 
in the same way as above """

for event_filter in example_object.event_filter_list:
	event_parameter_names = event_filter.get_all_parameter_names()
	print(event_parameter_names)

for trace_filter in example_object.trace_filter_list:
	trace_parameter_names = trace_filter.get_all_parameter_names()
	print(trace_parameter_names)
algorithm_parameter_names = example_object.algorithm.get_all_parameter_names()
print(algorithm_parameter_names)



""" You can access a lot of information from each parameter object, 
depending on the type. Please consider things like allowed ranges 
for time/numeric/integral parameters as well as the allowed set of 
options for selection type parameters. One specific calculation is
then done by the folling code:"""



import pandas as pd
from pm4py.objects.log.util import dataframe_utils
from pm4py.objects.conversion.log import converter as log_converter

log_csv = pd.read_csv('../data/BPI2016_Complaints.csv', sep=';')
log_csv = dataframe_utils.convert_timestamp_columns_in_df(log_csv)
log_csv = log_csv.sort_values('ContactDate')
log_csv.rename(columns={'ComplaintTopic_EN': 'concept:name', 'ContactDate': 'time:timestamp'}, inplace=True)
parameters = {log_converter.Variants.TO_EVENT_LOG.value.Parameters.CASE_ID_KEY: 'CustomerID'}
log = log_converter.apply(log_csv, parameters=parameters)
capsule_object = DataSetObject(log)

pipeLineObject.init_on_data_set(capsule_object)

from pprint import pprint
pprint(pipeLineObject.get_event_info_list())
pprint(pipeLineObject.get_trace_info_list())

