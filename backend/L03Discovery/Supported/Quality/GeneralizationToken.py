from L03Discovery.Supported.DiscoveryStepSuperClass import DiscoveryStepSuperClass
from pm4py.algo.evaluation.generalization.variants.token_based import apply


class GeneralizationToken(DiscoveryStepSuperClass):

    def __init__(self):
        super().__init__("Generalization, Token Variation",
                         "Measures how well the model generalizes based on if elements of the model were visited frequently enough."
                         " This is computed based on token-based replay of the log and the model."
                         " The resulting value is in the range between 0 and 1.",
                         apply)

    def execute_on_dataset(self, data_set):
        arguments = [data_set.original_data] + list(data_set.result)
        return self.method_callable(*arguments)
