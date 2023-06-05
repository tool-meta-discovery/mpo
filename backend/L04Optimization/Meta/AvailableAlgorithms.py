from enum import Enum


class AvailableAlgorithms(Enum):
    FixedRandomSearch = 0
    Bayesian = 1
    SimulatedAnnealing = 2
    NelderMead = 3

    @classmethod
    def has_value(cls, value):
        return value in AvailableAlgorithms.get_values()

    @classmethod
    def get_values(cls):
        return set(item for item in AvailableAlgorithms)
