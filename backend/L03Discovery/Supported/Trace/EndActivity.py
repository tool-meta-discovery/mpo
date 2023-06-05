from L03Discovery.Supported.DiscoveryStepSuperClass import DiscoveryStepSuperClass
from L02Parameter import *
import pm4py


class EndActivity(DiscoveryStepSuperClass):

	def __init__(self):

		super().__init__("End Activity","Specify end activities a trace must end on to be considered for discovery.",
						pm4py.filtering.filter_end_activities)
		self.parameter_list.append(self.create_attribute_parameter())

	def create_attribute_parameter(self):
		parameter = ParameterSelection("Activities","Select end activities.")
		return parameter

	def init_on_data_set(self,data_set_object):
		info_dict = pm4py.get_attribute_values(data_set_object.original_data,"concept:name")
		all_activities = [activity for activity,count in info_dict.items()]
		self.parameter_list[0].set_selection_set(all_activities)
		self.parameter_list[0].set_current_value(all_activities[0])

