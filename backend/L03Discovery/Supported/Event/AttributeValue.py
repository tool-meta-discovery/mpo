from L03Discovery.Supported.DiscoveryStepSuperClass import DiscoveryStepSuperClass
from L02Parameter import *
import pm4py
from pm4py.statistics.attributes.log.get import get_attribute_values


class AttributeValue(DiscoveryStepSuperClass):

	def __init__(self):

		super().__init__("Exclude Percentage Per Attribute","Filter based on the amount of occurences of a given attribute for each event.",
						pm4py.filtering.filter_event_attribute_values)
		self.parameter_list.append(self.create_percentage_parameter())
		self.parameter_list.append(self.create_attribute_parameter())

	def create_percentage_parameter(self):
		parameter = ParameterNumeric("Percentage","Specify percentage of values of the given attribute to keep for discovery.")
		parameter.set_current_value(1.0)
		parameter.set_lower_range(0.0)
		parameter.set_upper_range(1.0)
		return parameter

	def create_attribute_parameter(self):
		parameter = ParameterSelection("Attribute","Specify the attribute that is considered for the filter.")
		return parameter

	def init_on_data_set(self,data_set_object):
		all_attributes = pm4py.get_event_attributes(data_set_object.original_data)
		self.parameter_list[1].set_selection_set(all_attributes)
		self.parameter_list[1].set_current_value(all_attributes[0])

	def execute_on_dataset(self,data_set):
		info_dict = get_attribute_values(data_set.dataframe,self.parameter_list[1].current_value)
		info_dict_sorted = dict(reversed(sorted(info_dict.items(), key=lambda item: item[1])))
		all_counts = [count for value,count in info_dict_sorted.items()]
		total_count = sum(all_counts,0)
		for index in range(1,len(all_counts)):
			all_counts[index] += all_counts[index-1]
			if all_counts[index] >=total_count*self.parameter_list[0].current_value:
				break
		allowed_values = list(info_dict_sorted.keys())[:index]
		return self.method_callable(data_set.dataframe,self.parameter_list[1].current_value,allowed_values,level="event")


