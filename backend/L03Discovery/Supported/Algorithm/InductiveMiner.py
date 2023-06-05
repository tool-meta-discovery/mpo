from L03Discovery.Supported.DiscoveryStepSuperClass import DiscoveryStepSuperClass
from L02Parameter import *
from pm4py.algo.discovery.inductive.variants.im.algorithm import apply



class InductiveMiner(DiscoveryStepSuperClass):

	def __init__(self):

		super().__init__("Inductive Miner Algorithm",
						"The Inductive Miner discovers a process model with perfect replay fitness."
						" It was first introduced by Leemans, Fahland and van der Aalst.",
						apply)


