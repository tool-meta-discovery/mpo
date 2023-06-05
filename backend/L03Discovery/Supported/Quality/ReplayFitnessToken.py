from L03Discovery.Supported.DiscoveryStepSuperClass import DiscoveryStepSuperClass
from pm4py.algo.evaluation.replay_fitness.variants.token_replay import apply


class ReplayFitnessToken(DiscoveryStepSuperClass):

    def __init__(self):
        super().__init__("Replay Fitness, Token Variation",
                         "Measures the fitness of the resulting model computed with token-based replay."
                         " Only the fitness value of the complete log is considered."
                         " The resulting value is in the range between 0 and 1.",
                         apply)

    def execute_on_dataset(self, data_set):
        arguments = [data_set.original_data] + list(data_set.result)
        return self.method_callable(*arguments)["log_fitness"]
