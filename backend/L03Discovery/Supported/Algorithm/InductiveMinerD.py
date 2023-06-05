from L03Discovery.Supported.DiscoveryStepSuperClass import DiscoveryStepSuperClass
from L02Parameter import *
from pm4py.algo.discovery.inductive.variants.im_d.dfg_based import apply


class InductiveMinerD(DiscoveryStepSuperClass):

	def __init__(self):

		super().__init__("Inductive Miner Algorithm, Variant D",
						"The Inductive Miner Algorithm, Variant D only considers the directly-follows graph to achieve"
						" very good performance but has no guarantees for replay fitness."
						" It was first introduced by Leemans, Fahland and van der Aalst",
						apply)
