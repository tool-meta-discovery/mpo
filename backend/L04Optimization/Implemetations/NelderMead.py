import datetime
import math
import random
from random import Random

import pandas
from pandas.core.indexing import _LocIndexer

from L02Parameter import ParameterType

from L03Discovery.Capsules.DataSetObject import DataSetObject
from L03Discovery.Capsules.OptimizationObject import OptimizationObject
from L03Discovery.Supported.DiscoveryStepSuperClass import DiscoveryStepSuperClass
from L04Optimization.Implemetations.OptimizerImplementation import OptimizerImplementation


# this may not work out in the end

class NelderMead(OptimizerImplementation):
    """see: https://en.m.wikipedia.org/wiki/Nelder%E2%80%93Mead_method"""

    def __init__(self, optimization_object: OptimizationObject, data: DataSetObject):
        super().__init__(optimization_object, data, allow_parallel=False)
        self.rand = Random()
        self.rand.seed(123456789)

        self.time_frame_start = datetime.datetime.min
        self.time_frame_duration = datetime.timedelta.max

        self.n = len(self.get_all_optimization_parameters())
        self.vertices = pandas.DataFrame(columns=["quality"] + ["param_" + str(n) for n in range(self.n)])

        self.alpha = 1
        self.gamma = 3 # default: 2
        self.rho = 0.5
        self.sigma = 0.8 # default: 0.5
        # raise NotImplementedError("This Optimizer is not yet implemented!")

    def select_random_point(self):
        """sets all available parameters in the optimization object to random (but useful) values"""
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
        """randomly sets a timespan parameter"""
        parameter1 = parameter_collection.parameter_list[0]
        parameter2 = parameter_collection.parameter_list[1]
        lower = max(self.time_frame_start, parameter1.lower_range_end)
        random_range = min(self.time_frame_duration, parameter1.upper_range_end - lower)
        self.time_frame_start = rand.random() * random_range + lower
        self.time_frame_duration = rand.random() * (random_range - (self.time_frame_start - lower))
        parameter1.set_current_value(self.time_frame_start)
        parameter2.set_current_value(self.time_frame_start + self.time_frame_duration)

    def initialize_parameters(self, parameter_collection: DiscoveryStepSuperClass, rand: Random):
        """randomly sets all parameters"""
        for parameter_name in parameter_collection.get_all_parameter_names():
            parameter = parameter_collection.get_one_parameter(parameter_name)
            if parameter.value_type == ParameterType.FixedValue:
                continue
            elif parameter.value_type == ParameterType.Numeric:
                if parameter.upper_range_end == math.inf or parameter.lower_range_end == -math.inf:
                    raise ValueError("Upper and lower bounds need to be set!")
                else:
                    random_range = parameter.upper_range_end - parameter.lower_range_end
                    parameter.set_current_value(rand.random() * random_range + parameter.lower_range_end)
            elif parameter.value_type == ParameterType.Integral:
                if parameter.upper_range_end == math.inf or parameter.lower_range_end ==-math.inf:
                    raise ValueError("Upper and lower bounds need to be set!")
                else:
                    random_range = int(parameter.upper_range_end - parameter.lower_range_end)
                    parameter.set_current_value(int(rand.random() * random_range + parameter.lower_range_end))
            elif parameter.value_type == ParameterType.Selection:
                parameter.set_current_value(random.choice(parameter.get_selection_set()))
            elif parameter.value_type == ParameterType.Time:
                random_range = parameter.upper_range_end - parameter.lower_range_end
                parameter.set_current_value(rand.random() * random_range + parameter.lower_range_end)

    def access_vertex(self, i) -> _LocIndexer:
        return self.vertices.iloc[i, 1:]

    def get_vertex_as_np(self, i):
        return self.access_vertex(i).to_numpy()

    def update_vertex(self, i, score, vertex):
        self.vertices.iloc[i, 0] = score
        self.vertices.iloc[i, 1:] = vertex

    def iterate(self):
        if self.n == 0:  # early-out for 0-dimensional parameter space
            self.optimization.execute_on_dataset(self.data)
            self.log_discovery(self.data)
            return
        # at start we have no aquisition function, so we create one sample
        while len(self.vertices) < self.n + 1:
            self.select_random_point()
            quality = self.calculate_objective_function(self.encode_parameters())
            params = self.encode_parameters()
            self.vertices = pandas.concat(
                [self.vertices, pandas.DataFrame(columns=["quality"] + ["param_" + str(n) for n in range(self.n)],
                                                 data=[[quality] + params])])
        # sort and df cleaning
        self.vertices.sort_values(inplace=True, by="quality", ascending=False)
        self.vertices.reset_index(inplace=True)
        self.vertices.drop(columns="index", inplace=True)
        # quick access to specific values
        worst = self.get_vertex_as_np(-1)
        best_score = self.vertices.iloc[0, 0]
        second_worst_score = self.vertices.iloc[-2, 0]
        worst_score = self.vertices.iloc[-1, 0]
        # centroid calculation
        centroid = self.vertices.drop(columns=["quality"]).mean(axis=0).to_numpy()
        # reflection calculation
        x_r = centroid + self.alpha * (centroid - worst)
        reflect_score = self.calculate_objective_function(x_r)
        if best_score > reflect_score >= second_worst_score:
            self.update_vertex(-1, reflect_score, x_r)
            # self.vertices.loc[-1, "quality"] = reflect_score
            # self.vertices.loc[-1, "vertex"] = x_r
            return
        # expansion calculation
        if best_score < reflect_score:
            x_e = centroid + self.gamma * (centroid - worst)
            expand_score = self.calculate_objective_function(x_e)
            if expand_score > reflect_score:
                self.update_vertex(-1, expand_score, x_e)
                # self.vertices.loc[-1, "quality"] = expand_score
                # self.vertices.loc[-1, "vertex"] = x_e
                return
            else:
                self.update_vertex(-1, reflect_score, x_r)
                # self.vertices.loc[-1, "quality"] = reflect_score
                # self.vertices.loc[-1, "vertex"] = x_r
                return
        # contraction calculation
        if reflect_score > self.vertices.iloc[-1, 0]:
            x_c = centroid + self.rho * (x_r - centroid)
            contract_score = self.calculate_objective_function(x_c)
            if contract_score > reflect_score:
                self.update_vertex(-1, contract_score, x_c)
                # self.vertices.loc[-1, "quality"] = contract_score
                # self.vertices.loc[-1, "vertex"] = x_c
                return
        else:
            x_c = centroid + self.rho * (worst - centroid)
            contract_score = self.calculate_objective_function(x_c)
            if contract_score > worst_score:
                self.update_vertex(-1, contract_score, x_c)
                # self.vertices.loc[-1, "quality"] = contract_score
                # self.vertices.loc[-1, "vertex"] = x_c
                return
        # shrinking calculation
        x_1 = self.get_vertex_as_np(0)
        for row_nr in range(1, self.vertices.shape[0]):
            x_n = x_1 + self.sigma * (self.get_vertex_as_np(row_nr) - x_1)
            self.update_vertex(row_nr, self.calculate_objective_function(x_n), x_n)

    def calculate_objective_function(self, x):
        self.decode_parameters(x)
        self.optimization.execute_on_dataset(self.data)
        self.log_discovery(self.data)
        return self.data.score

    def get_workers(self, worker_count: int):
        if worker_count > 1:
            raise ValueError("Can only create one worker.")
        return [self.iterate for i in range(worker_count)]
