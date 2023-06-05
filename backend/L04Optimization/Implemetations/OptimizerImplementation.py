import datetime
from typing import List
from typing import Callable
from copy import deepcopy

import pandas

from L02Parameter import ParameterType
from L03Discovery.Capsules.OptimizationObject import OptimizationObject
from L03Discovery.Capsules.DataSetObject import DataSetObject
from L03Discovery.Supported.DiscoveryStepSuperClass import DiscoveryStepSuperClass


class OptimizerImplementation:
    allow_parallel: bool
    optimization: OptimizationObject
    data: DataSetObject
    history: pandas.DataFrame

    def __init__(self, optimization_object: OptimizationObject, data: DataSetObject, allow_parallel: bool = True):
        self.optimization = optimization_object
        self.history = pandas.DataFrame(columns=["quality", "result"])
        self.data = data
        self.allow_parallel = allow_parallel
        pass

    def iterate(self):
        pass

    def get_best_quality(self):
        return self.history["quality"].max()

    def get_best(self) -> pandas.DataFrame:
        return self.history.sort_values(by="quality", ascending=False).iloc[0]

    def log_discovery(self, discovery: DataSetObject):
        """writes a history row for the current parameter settings and quality measurements"""
        self.history = pandas.concat([self.history, pandas.DataFrame(
            [[discovery.score, discovery.result, discovery.score_dict, self.optimization.algorithm.name]],
            columns=["quality", "result", "details", "algorithm"])])
        for trace_filter in self.optimization.trace_filter_list:
            self.log_parameters(trace_filter)
        for event_filter in self.optimization.event_filter_list:
            self.log_parameters(event_filter)
        self.log_parameters(self.optimization.algorithm)

    def log_parameters(self, parameter_collection: DiscoveryStepSuperClass):
        """fills the current history line with the current parameter settings"""
        for parameter_name in parameter_collection.get_all_parameter_names():
            parameter = parameter_collection.get_one_parameter(parameter_name)
            prefix = parameter_collection.name + ": "
            if prefix + parameter_name not in self.history.columns:
                if parameter.value_type != ParameterType.Time:
                    self.history.insert(2, prefix + parameter_name, parameter.current_value, True)
                else:
                    self.history.insert(2, prefix + parameter_name, parameter.current_value.isoformat(), True)
            else:
                if parameter.value_type != ParameterType.Time:
                    self.history.loc[self.history.index[-1], prefix + parameter_name] = parameter.current_value
                else:
                    self.history.loc[self.history.index[-1], prefix + parameter_name] = \
                        parameter.current_value.isoformat()

    def is_parallel_allowed(self):
        return self.allow_parallel

    def get_workers(self, worker_count: int) -> List[Callable]:
        pass

    def get_all_optimization_parameters(self) -> List:
        """returns a list of all parameters for optimization"""
        parameters = list()
        for trace_filter in self.optimization.trace_filter_list:
            parameters.extend([trace_filter.get_one_parameter(name) for name
                               in trace_filter.get_all_parameter_names()])
        for event_filter in self.optimization.event_filter_list:
            parameters.extend([event_filter.get_one_parameter(name) for name
                               in event_filter.get_all_parameter_names()])
        parameters.extend([self.optimization.algorithm.get_one_parameter(name) for name
                           in self.optimization.algorithm.get_all_parameter_names()])
        return parameters

    def encode_parameters(self):
        """creates a list with numeric representations of all current parameters"""
        x = list()
        for parameter in self.get_all_optimization_parameters():
            if parameter.value_type == ParameterType.FixedValue:
                continue
            elif parameter.value_type == ParameterType.Numeric or parameter.value_type == ParameterType.Integral:
                x.append(parameter.current_value)
            elif parameter.value_type == ParameterType.Time:
                dt: datetime.timedelta = parameter.current_value - datetime.datetime.min
                try:
                    x.append(dt.total_seconds())
                except:
                    print("ERROR")
            elif parameter.value_type == ParameterType.Selection:
                x.append(int(parameter.get_selection_set().index(parameter.current_value)))

        return x

    def decode_parameters(self, x):
        """set the current parameter settings from a list of numeric representations"""
        idx = 0
        for parameter in self.get_all_optimization_parameters():
            if parameter.value_type == ParameterType.FixedValue:
                continue
            elif parameter.value_type == ParameterType.Numeric:
                if parameter.lower_range_end > x[idx]:
                    parameter.set_current_value(parameter.lower_range_end)
                elif parameter.upper_range_end < x[idx]:
                    parameter.set_current_value(parameter.upper_range_end)
                else:
                    parameter.set_current_value(x[idx])
            elif parameter.value_type == ParameterType.Integral:
                if parameter.lower_range_end > x[idx]:
                    parameter.set_current_value(parameter.lower_range_end)
                elif parameter.upper_range_end < x[idx]:
                    parameter.set_current_value(parameter.upper_range_end)
                else:
                    parameter.set_current_value(int(x[idx]))
            elif parameter.value_type == ParameterType.Time:
                ts = x[idx]
                dt: datetime.datetime = datetime.datetime.min
                dt += datetime.timedelta(seconds=ts)
                if parameter.lower_range_end > dt:
                    parameter.set_current_value(parameter.lower_range_end)
                elif parameter.upper_range_end < dt:
                    parameter.set_current_value(parameter.upper_range_end)
                else:
                    parameter.set_current_value(dt)
            elif parameter.value_type == ParameterType.Selection:
                parameter.set_current_value(parameter.get_selection_set()[max(int(x[idx]),len(parameter.get_selection_set())-1)])
            idx += 1