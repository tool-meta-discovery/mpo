from L03Discovery.Supported.DiscoveryStepSuperClass import DiscoveryStepSuperClass
from L02Parameter import *
import pm4py


class FrequentVariants(DiscoveryStepSuperClass):

	def __init__(self):

		super().__init__("Frequent Variants","Filter on the frequency of trace variants.",
						pm4py.filtering.filter_variants_top_k)
		self.parameter_list.append(self.create_k_attribute())

	def create_k_attribute(self):
		parameter = ParameterIntegral("Frequency","Specify a frequency range.")
		parameter.set_current_value(1)
		parameter.set_lower_range(1)
		parameter.set_upper_range(100)
		return parameter

