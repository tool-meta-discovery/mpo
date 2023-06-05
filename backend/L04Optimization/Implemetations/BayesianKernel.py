import datetime
import math
import random
from random import Random
from typing import Any

import numpy as np
from scipy.stats import norm
from sklearn.gaussian_process import GaussianProcessRegressor

from L02Parameter import ParameterType
from L03Discovery.Capsules.DataSetObject import DataSetObject
from L03Discovery.Capsules.OptimizationObject import OptimizationObject
from L03Discovery.Supported.DiscoveryStepSuperClass import DiscoveryStepSuperClass
from L04Optimization.Implemetations.OptimizerImplementation import OptimizerImplementation


# for now this is scrapped in favor of basic bayesian optimizer

class BayesianKernel(OptimizerImplementation):

    def __init__(self, optimization_object: OptimizationObject, data: DataSetObject):
        super().__init__(optimization_object, data, allow_parallel=False)
        self.rand = Random()
        # self.rand.seed(123456789)
        self.select_random_point()
        self.x_list = list()
        self.y_list = list()
        self.regressor = GaussianProcessRegressor()
        self.time_frame_start = datetime.datetime.min
        self.time_frame_duration = datetime.timedelta.max
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
            if parameter.value_type == ParameterType.FixedValue:
                continue
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

    def approximation(self, x):
        return self.regressor.predict(x, return_std=True)
        # return self.regressor.predict(x)

    def acquisition(self, x, x_samples):
        # yhat = self.approximation(x)
        yhat, _ = self.approximation(x)
        best = max(yhat)

        mu, std = self.approximation(x_samples)
        # mu = self.approximation(x_samples)
        # mu = mu[:, 0]
        probs = norm.cdf((mu - best) / (std + 1E-9))
        return probs

    def opt_acquisition(self, x) -> Any:
        # create random sampling points
        x_sample = list()
        for i in range(50):
            self.select_random_point()
            x_sample.append(self.encode_parameters())
        scores = self.acquisition(x, x_sample)
        ix = np.argmax(scores)
        return x_sample[ix]

    def iterate(self):
        # at start we have no aquisition function, so we create one sample
        if len(self.x_list) == 0:
            self.x_list.append(self.encode_parameters())
            self.optimization.execute_on_dataset(self.data)
            self.log_discovery(self.data)
            self.y_list.append(self.data.score)
            self.regressor.fit(np.array(self.x_list).reshape(1, -1), self.y_list)
        # acquisition
        x_test = self.opt_acquisition(np.array(self.encode_parameters()).reshape(1, -1))
        self.decode_parameters(x_test)
        # sample
        self.x_list.append(x_test)
        self.optimization.execute_on_dataset(self.data)
        self.log_discovery(self.data)
        self.y_list.append(self.data.score)
        # update gaussian model
        self.regressor.fit(self.x_list, self.y_list)

    def calculate_objective_function(self, x):
        self.decode_parameters(x)
        self.optimization.execute_on_dataset(self.data)
        self.log_discovery(self.data)
        return self.data.score

    def get_workers(self, worker_count: int):
        if worker_count > 1:
            raise ValueError("Can only create one worker.")
        return [self.iterate for i in range(worker_count)]
