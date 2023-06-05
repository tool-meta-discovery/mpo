import math
import random
from random import Random
import datetime
from L04Optimization.Implemetations.OptimizerImplementation import  OptimizerImplementation
from L02Parameter.Enumeration.ParameterType import ParameterType
from L03Discovery.Capsules.DataSetObject import DataSetObject
from L03Discovery.Capsules.OptimizationObject import OptimizationObject
from L03Discovery.Supported.DiscoveryStepSuperClass import DiscoveryStepSuperClass


class FixedRandomSearch(OptimizerImplementation):

    def __init__(self, optimization_object: OptimizationObject, data: DataSetObject):
        super().__init__(optimization_object, data)

    def iterate(self):
        rand = Random(datetime.datetime.utcnow())
        rand.seed(123456789)
        # setup trace filter with randomized uncertain parameters
        for trace_filter in self.optimization.trace_filter_list:
            self.fill_parameters(trace_filter, rand)
        # setup event filter with randomized uncertain parameters
        for event_filter in self.optimization.event_filter_list:
            self.fill_parameters(event_filter, rand)
        # setup model with randomized uncertain parameters
        self.fill_parameters(self.optimization.algorithm, rand)
        # execute
        self.optimization.execute_on_dataset(self.data)
        self.log_discovery(self.data)
        pass

    def fill_parameters(self, parameter_collection: DiscoveryStepSuperClass, rand: Random):
        for parameter_name in parameter_collection.get_all_parameter_names():
            parameter = parameter_collection.get_one_parameter(parameter_name)
            if parameter.value_type == ParameterType.FixedValue:
                continue
            elif parameter.value_type == ParameterType.Numeric:
                if parameter.upper_range_end == math.inf or parameter.lower_range_end == -math.inf:
                    raise ValueError("Upper and lower bounds need to be set!")
                else:
                    random_range = parameter.upper_range_end-parameter.lower_range_end
                    parameter.set_current_value(rand.random()*random_range + parameter.lower_range_end)
            elif parameter.value_type == ParameterType.Integral:
                if parameter.upper_range_end == int(math.inf) or parameter.lower_range_end == int(-math.inf):
                    raise ValueError("Upper and lower bounds need to be set!")
                else:
                    random_range = int(parameter.upper_range_end-parameter.lower_range_end)
                    parameter.set_current_value(int(rand.random()*random_range + parameter.lower_range_end))
            elif parameter.value_type == ParameterType.Selection:
                parameter.set_current_value(random.choice(parameter.get_selection_set()))
            elif parameter.value_type == ParameterType.Time:
                random_range = parameter.upper_range_end-parameter.lower_range_end
                parameter.set_current_value(rand.random()*random_range + parameter.lower_range_end)

    def get_workers(self, worker_count: int):
        return [self.iterate for i in range(worker_count)]
