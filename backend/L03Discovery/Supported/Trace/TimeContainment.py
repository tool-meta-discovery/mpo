from L03Discovery.Supported.DiscoveryStepSuperClass import DiscoveryStepSuperClass
from L02Parameter import *
from pm4py.algo.filtering.log.timestamp import timestamp_filter
from pm4py.statistics.attributes.log.get import *

class TimeContainment(DiscoveryStepSuperClass):

	def __init__(self):


		super().__init__("Time Frame Containment Filter",
						"You can use this filter to only include traces that fall completely into the" 
						" specified time interval. All other traces, even if only one of their events is "
						" outside the interval, will be discarded for the optimization process.",
						timestamp_filter.filter_traces_contained)

		self.parameter_list.append(self.create_lower_bound_parameter())
		self.parameter_list.append(self.create_upper_bound_parameter())


	def create_lower_bound_parameter(self):
		parameter = ParameterTime("Lower Time Bound",
											"You can use this parameter to specifiy the lower bound for the selected"
											" time interval filtering. All traces with events occuring before this date"
											" time will be discarded for the optimization process.")
		parameter.set_current_value(parameter.lower_range_end)
		return parameter


	def create_upper_bound_parameter(self):
		parameter = ParameterTime("Upper Time Bound",
											"You can use this parameter to specifiy the upper bound for the selected"
											" time interval filtering. All traces with events occuring after this date "
											" time will be discarded for the optimization process.")
		parameter.set_current_value(parameter.upper_range_end)
		return parameter


	def init_on_data_set(self,data_set_object):
		info_dict = get_attribute_values(data_set_object.original_data, "time:timestamp")
		all_stamps = [stamp.to_pydatetime().replace(tzinfo=None) for stamp,count in info_dict.items()]
		self.parameter_list[0].set_current_value(min(all_stamps))
		self.parameter_list[0].set_lower_range(min(all_stamps))
		self.parameter_list[0].set_upper_range(max(all_stamps))
		self.parameter_list[1].set_current_value(max(all_stamps))
		self.parameter_list[1].set_lower_range(min(all_stamps))
		self.parameter_list[1].set_upper_range(max(all_stamps))