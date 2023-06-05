from L03Discovery.Supported.DiscoveryStepSuperClass import DiscoveryStepSuperClass
from L02Parameter import *
from pm4py.algo.discovery.inductive.variants.im_f.algorithm import apply,Parameters


class InductiveMinerF(DiscoveryStepSuperClass):

	def __init__(self):

		super().__init__("Inductive Miner Algorithm, F Variant",
						"The Inductive Miner Variant F aims to obtain a more precise model by removing some infrequent behavior."
						" It was first introduced by Leemans, Fahland and van der Aalst",
						apply)
		self.parameter_list.append(self.create_noise_parameter())


	def create_noise_parameter(self):
		parameter = ParameterNumeric("Noise Threshold","Specify boundaries to the search space of the Noise Threshold parameter.")
		parameter.set_current_value(0.2)
		parameter.set_lower_range(0.0)
		parameter.set_upper_range(1.0)
		return parameter

	def execute_on_dataset(self,data_set):
		return self.method_callable(data_set.dataframe,{Parameters.NOISE_THRESHOLD:self.parameter_list[0].current_value})


