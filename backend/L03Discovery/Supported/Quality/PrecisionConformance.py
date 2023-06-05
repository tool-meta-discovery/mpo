from L03Discovery.Supported.DiscoveryStepSuperClass import DiscoveryStepSuperClass
from pm4py.algo.evaluation.precision.variants.etconformance_token import apply


class PrecisionConformance(DiscoveryStepSuperClass):

    def __init__(self):
        super().__init__("Precision, ETC Conformance Variant",
                         "Measures the precision of the resulting model computed with token-based replay."
                         " The resulting value is in the range between 0 and 1.",
                         apply)

    def execute_on_dataset(self, data_set):
        arguments = [data_set.original_data] + list(data_set.result)
        return self.method_callable(*arguments)
