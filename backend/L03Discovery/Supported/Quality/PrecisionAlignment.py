from L03Discovery.Supported.DiscoveryStepSuperClass import DiscoveryStepSuperClass
from pm4py.algo.evaluation.precision.variants.align_etconformance import apply


class PrecisionAlignment(DiscoveryStepSuperClass):

    def __init__(self):
        super().__init__("Precision, Alignment Variant",
                         "Measures the precision of the resulting model based on alignments."
                         " The resulting value is in the range between 0 and 1.",
                         apply)

    def execute_on_dataset(self, data_set):
        arguments = [data_set.original_data] + list(data_set.result)
        return self.method_callable(*arguments)
