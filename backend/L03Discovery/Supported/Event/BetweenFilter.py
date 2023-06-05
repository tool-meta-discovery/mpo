from L03Discovery.Supported.DiscoveryStepSuperClass import DiscoveryStepSuperClass
from L02Parameter import *
import pm4py
from pm4py.statistics.attributes.log.get import get_attribute_values


class BetweenFilter(DiscoveryStepSuperClass):

	def __init__(self):

		super().__init__("Between Filter",
						"You can use this filter to only include traces that include the given transition.",
						pm4py.filtering.filter_between)

		self.parameter_list.append(self.first_event_parameter())
		self.parameter_list.append(self.second_event_parameter())

	def first_event_parameter(self):
		parameter = ParameterSelection("Source Activity","Specify a source activity of the transition.")
		return parameter

	def second_event_parameter(self):
		parameter = ParameterSelection("Target Activity","Specify the target activity of the transition.")
		return parameter

	def init_on_data_set(self,data_set_object):
		info_dict = get_attribute_values(data_set_object.original_data, "concept:name")
		info_dict_sorted = dict(reversed(sorted(info_dict.items(), key=lambda item: item[1])))
		all_activities = list(info_dict_sorted.keys())
		self.parameter_list[0].set_selection_set(all_activities)
		self.parameter_list[0].set_current_value(all_activities[0])
		self.parameter_list[1].set_selection_set(all_activities)
		self.parameter_list[1].set_current_value(all_activities[1])

