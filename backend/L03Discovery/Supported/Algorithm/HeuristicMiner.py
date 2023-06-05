from L03Discovery.Supported.DiscoveryStepSuperClass import DiscoveryStepSuperClass
from L02Parameter import *
from pm4py.algo.discovery.heuristics.variants.classic import apply,Parameters


class HeuristicMiner(DiscoveryStepSuperClass):

	def __init__(self):

		super().__init__("Heuristic Miner Algorithm, Classic Variant",
						"The Heuristic Miner discovers process models based on the directly follows relation. Therefore,"
						" frequency of directly follows relations are considered to deal with noise in the data."
						" It was first introduced by van der Aalst and Weijters.",
						apply)

		self.parameter_list.append(self.create_dependecy_parameter())
		self.parameter_list.append(self.create_measrue_parameter())
		self.parameter_list.append(self.create_act_count_parameter())
		self.parameter_list.append(self.create_dfg_occurence_parameter())
		self.parameter_list.append(self.create_noise_parameter())


	def create_dependecy_parameter(self):
		parameter = ParameterNumeric("Dependency Threshold","Specify boundaries to the search space"
															" of the Dependency Threshold parameter.")
		parameter.set_current_value(0.5)
		parameter.set_lower_range(0.0)
		parameter.set_upper_range(1.0)
		return parameter

	def create_measrue_parameter(self):
		parameter = ParameterNumeric("AND Measure Threshold","Specify boundaries to the search"
															 " space of the AND Measure Threshold.")
		parameter.set_current_value(0.65)
		parameter.set_lower_range(0.0)
		parameter.set_upper_range(1.0)
		return parameter

	def create_act_count_parameter(self):
		parameter = ParameterIntegral("Minimum Activity Count","Specify boundaries to the search"
															   " space of the Minimum Activity Count parameter.")
		parameter.set_current_value(1)
		parameter.set_lower_range(1)
		parameter.set_upper_range(9999)
		return parameter

	def create_dfg_occurence_parameter(self):
		parameter = ParameterIntegral("Minimum DFG Occurence", "Specify boundaries to the search"
															   " space of the Minimum DFG Occurence parameter.")
		parameter.set_current_value(1)
		parameter.set_lower_range(1)
		parameter.set_upper_range(9999)
		return parameter

	def create_noise_parameter(self):
		parameter = ParameterNumeric("Noise Threshold", "Specifiy boundaries to the search space of the Noise Threshold.")
		parameter.set_current_value(0.05)
		parameter.set_lower_range(0.0)
		parameter.set_upper_range(1.0)
		return parameter

	def execute_on_dataset(self,data_set):

		parameters = {
			Parameters.DEPENDENCY_THRESH :self.parameter_list[0].current_value,
			Parameters.AND_MEASURE_THRESH :self.parameter_list[1].current_value,
			Parameters.MIN_ACT_COUNT:self.parameter_list[2].current_value,
			Parameters.MIN_DFG_OCCURRENCES :self.parameter_list[3].current_value,
			Parameters.DFG_PRE_CLEANING_NOISE_THRESH :self.parameter_list[4].current_value,
		}

		return self.method_callable(data_set.dataframe,parameters)


