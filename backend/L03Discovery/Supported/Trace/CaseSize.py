from L03Discovery.Supported.DiscoveryStepSuperClass import DiscoveryStepSuperClass
from L02Parameter import *
import pm4py


class CaseSize(DiscoveryStepSuperClass):

	def __init__(self):

		super().__init__("Case Runtime","Filter based on the runtime of a case.",
						pm4py.filtering.filter_case_size)
		self.parameter_list.append(self.create_min_attribute())
		self.parameter_list.append(self.create_max_attribute())

	def create_min_attribute(self):
		parameter = ParameterIntegral("Minimum Runtime","Specify a lower bound of considered runtime."
														"Default value is minimum found in the log.")
		parameter.set_current_value(1)
		parameter.set_lower_range(1)
		parameter.set_upper_range(100)
		return parameter

	def create_max_attribute(self):
		parameter = ParameterIntegral("Maximum Runtime","Specify a upper bound of the considered runtime."
														"Default value is maximum found in the log.")
		parameter.set_current_value(100)
		parameter.set_lower_range(1)
		parameter.set_upper_range(100)
		return parameter

