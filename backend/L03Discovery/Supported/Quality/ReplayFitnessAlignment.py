from L03Discovery.Supported.DiscoveryStepSuperClass import DiscoveryStepSuperClass
from pm4py.algo.evaluation.replay_fitness.variants.alignment_based import apply


class ReplayFitnessAlignment(DiscoveryStepSuperClass):

    def __init__(self):
        super().__init__("Replay Fitness, Alignment Variation",
                         "Measures the fitness of the resulting model based alignments."
                         " Only the fitness value of the complete log is considered."
                         " The resulting value is in the range between 0 and 1.",
                         apply)

    def execute_on_dataset(self, data_set):
        arguments = [data_set.original_data] + list(data_set.result)
        return self.method_callable(*arguments)["log_fitness"]
