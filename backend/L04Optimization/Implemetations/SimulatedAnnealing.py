import datetime
import math
import random
from random import Random

from L02Parameter import ParameterType

from L03Discovery.Capsules.DataSetObject import DataSetObject
from L03Discovery.Capsules.OptimizationObject import OptimizationObject
from L03Discovery.Supported.DiscoveryStepSuperClass import DiscoveryStepSuperClass
from L04Optimization.Implemetations.OptimizerImplementation import OptimizerImplementation


# this may not work out in the end

class SimulatedAnnealing(OptimizerImplementation):

    def __init__(self, optimization_object: OptimizationObject, data: DataSetObject):
        super().__init__(optimization_object, data, allow_parallel=False)
        self.rand = Random()
        self.rand.seed(123456789)
        self.k = 0
        self.k_max = 200
        self.current_energy = math.inf
        self.s = None
        self.T_max = 1 # 10: max prop @ diff 0.1 is ~98%
        self.time_frame_start = datetime.datetime.min
        self.time_frame_duration = datetime.timedelta.max
        self.max_time = None
        self.start_time = None
        self.select_random_point()
        if __debug__:
            self.temps = list()
            self.props = list()
            self.delta_e = list()
        # raise NotImplementedError("This Optimizer is not yet implemented!")

    def select_random_point(self):
        from L03Discovery.Supported.Trace.TimeContainment import TimeContainment as TraceTimeContainment
        from L03Discovery.Supported.Event.TimeContainment import TimeContainment as EventTimeContainment

        self.time_frame_start = datetime.datetime.min
        self.time_frame_duration = datetime.timedelta.max

        for trace_filter in self.optimization.trace_filter_list:
            if isinstance(trace_filter, TraceTimeContainment):
                self.initialize_timespan_parameters(trace_filter, self.rand)
            else:
                self.initialize_parameters(trace_filter, self.rand)
        for event_filter in self.optimization.event_filter_list:
            if isinstance(event_filter, EventTimeContainment):
                self.initialize_timespan_parameters(event_filter, self.rand)
            else:
                self.initialize_parameters(event_filter, self.rand)
        self.initialize_parameters(self.optimization.algorithm, self.rand)

    def initialize_timespan_parameters(self, parameter_collection: DiscoveryStepSuperClass, rand: Random):
        parameter1 = parameter_collection.parameter_list[0]
        parameter2 = parameter_collection.parameter_list[1]
        lower = max(self.time_frame_start, parameter1.lower_range_end)
        random_range = min(self.time_frame_duration, parameter1.upper_range_end - lower)
        self.time_frame_start = rand.random() * random_range + lower
        self.time_frame_duration = rand.random() * (random_range - (self.time_frame_start - lower))
        parameter1.set_current_value(self.time_frame_start)
        parameter2.set_current_value(self.time_frame_start+self.time_frame_duration)

    def initialize_parameters(self, parameter_collection: DiscoveryStepSuperClass, rand: Random):
        for parameter_name in parameter_collection.get_all_parameter_names():
            parameter = parameter_collection.get_one_parameter(parameter_name)
            self.set_parameter_randomly(parameter, rand)

    def set_parameter_randomly(self, parameter, rand):
        if parameter.value_type == ParameterType.FixedValue:
            return
        elif parameter.value_type == ParameterType.Numeric:
            if parameter.upper_range_end == math.inf or parameter.lower_range_end == -math.inf:
                raise ValueError("Upper and lower bounds need to be set!")
            else:
                random_range = parameter.upper_range_end - parameter.lower_range_end
                parameter.set_current_value(rand.random() * random_range + parameter.lower_range_end)
        elif parameter.value_type == ParameterType.Integral:
            if parameter.upper_range_end == int(math.inf) or parameter.lower_range_end == int(-math.inf):
                raise ValueError("Upper and lower bounds need to be set!")
            else:
                random_range = int(parameter.upper_range_end - parameter.lower_range_end)
                parameter.set_current_value(int(rand.random() * random_range + parameter.lower_range_end))
        elif parameter.value_type == ParameterType.Selection:
            parameter.set_current_value(random.choice(parameter.get_selection_set()))
        elif parameter.value_type == ParameterType.Time:
            random_range = parameter.upper_range_end - parameter.lower_range_end
            parameter.set_current_value(rand.random() * random_range + parameter.lower_range_end)

    def temperature(self) -> float:
        # time adaptive temperature change
        if self.max_time is not None:
            runtime = datetime.datetime.now() - self.start_time
            T = max([self.T_max * (1 - (runtime / self.max_time)), 0.001])
        else:
            T = max([self.T_max * (1 - (self.k / self.k_max)), 0.001])
        if __debug__:
            self.temps.append(T)
        return T

    def neighbor(self):
        for i in range(2):
            parameter = self.rand.choice(self.get_all_optimization_parameters())
            self.set_parameter_randomly(parameter, self.rand)

    def iterate(self):
        if self.start_time is None:
            self.start_time = datetime.datetime.now()
        self.s = self.encode_parameters()
        self.neighbor()
        e_new = self.calculate_loss()
        if __debug__:
            self.delta_e.append(e_new - self.current_energy)
        p = self.calculate_switch_pobability(e_new)
        if __debug__:
            self.props.append(p)
        if p < self.rand.random():
            self.decode_parameters(self.s)
        else:
            self.current_energy = e_new
        self.k += 1

    def calculate_switch_pobability(self, e_new):
        p = math.exp(- ((e_new - self.current_energy) / self.temperature()))
        if e_new < self.current_energy:
            return 1
        else:
            return p



    def calculate_loss(self):
        self.optimization.execute_on_dataset(self.data)
        self.log_discovery(self.data)
        return 1- self.data.score

    def get_workers(self, worker_count: int):
        if worker_count > 1:
            raise ValueError("Can only create one worker.")
        return [self.iterate for i in range(worker_count)]
