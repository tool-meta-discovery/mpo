from L03Discovery.Supported.DiscoveryStepSuperClass import DiscoveryStepSuperClass
from L02Parameter import *
from pm4py.algo.discovery.alpha.variants.classic import apply


class AlphaMiner(DiscoveryStepSuperClass):

	def __init__(self):

		super().__init__("Alpha Miner Algorithm, Classic Variant",
						"The Alpha Miner creates a workflow net based on the directly follows relation."
						" It was first introduced by van der Aalst, Weijters and Maruster",
						apply)

