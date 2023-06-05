from L03Discovery.Supported.DiscoveryStepSuperClass import DiscoveryStepSuperClass
from pm4py.algo.evaluation.simplicity.variants.arc_degree import apply


class SimplicityArcDegree(DiscoveryStepSuperClass):

    def __init__(self):
        super().__init__("Simplicity, Arc Degree Variant",
                         "Simplicity is evaluated solely on the mined petri net."
                         " Therefore the inverse arc degree of places and transitions is considered."
                         " The resulting value is in the range between 0 and 1.",
                         apply)

    def execute_on_dataset(self, data_set):
        arguments = [list(data_set.result)[0]]
        return self.method_callable(*arguments)
