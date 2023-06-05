import datetime
from typing import Callable, List, Union

import pandas

from L03Discovery.Capsules.DataSetObject import DataSetObject
from L04Optimization.Implemetations.NelderMead import NelderMead
from L04Optimization.Meta.AvailableAlgorithms import AvailableAlgorithms
from L04Optimization.Implemetations.OptimizerImplementation import OptimizerImplementation
from L04Optimization.Implemetations.FixedRandomSearch import FixedRandomSearch
from L04Optimization.Implemetations.BayesianKernel import BayesianKernel
from L04Optimization.Implemetations.SimulatedAnnealing import SimulatedAnnealing
from L03Discovery.Capsules.OptimizationObject import OptimizationObject


class Optimizer:
    """This class manages the optimization of process discovery pipeline meta parameters.
    The algorithm used by default is FixedRandomSearch.
    The default quality threshold is 1."""
    algorithm: AvailableAlgorithms
    allow_next_iteration: bool
    quality_threshold: float
    optimizer: OptimizerImplementation
    data: DataSetObject
    optimization: OptimizationObject
    start_time: datetime.datetime
    max_runtime: datetime.timedelta

    def __init__(self):
        self.worker = None
        self.algorithm = AvailableAlgorithms.NelderMead
        self.allow_next_iteration = True
        self.quality_threshold = 1
        self.max_runtime = datetime.timedelta.max
        self.iter_no = 0

    def set_optimization(self, optimization_object: OptimizationObject):
        """Sets the optimization object containing what should be optimized."""
        self.optimization = optimization_object

    def with_optimization(self, optimization_object: OptimizationObject):
        """Sets the optimization object containing what should be optimized.
        Returns the optimizer for chaining setup calls (e.g. optimizer.with_optimization(x).start())"""
        self.set_optimization(optimization_object)
        return self

    def set_algorithm(self, algorithm_type: AvailableAlgorithms):
        """Sets the algorithm to use for optimization."""
        if not AvailableAlgorithms.has_value(algorithm_type):
            raise ValueError("algorithm type was not selected from "
                             "L12Optimization.Meta.AvailableAlgorithms.AvailableAlgorithms")
        self.algorithm = algorithm_type

    def with_algorithm(self, algorithm_type: AvailableAlgorithms):
        """Sets the algorithm to use for optimization.
        Returns the optimizer for chaining setup calls (e.g. optimizer.with_algorithm(x).start())"""
        self.set_algorithm(algorithm_type)
        return self

    def set_dataset(self, dataset: DataSetObject):
        """Sets the dataset to use for optimization."""
        self.data = dataset

    def with_dataset(self, dataset: DataSetObject):
        """Sets the dataset to use for optimization.
        Returns the optimizer for chaining setup calls (e.g. optimizer.with_dataset(x).start())"""
        self.set_dataset(dataset)
        return self

    def set_quality_threshold(self, quality_threshold: float):
        """Sets the quality threshold to use for optimization termination."""
        self.quality_threshold = quality_threshold

    def with_quality_threshold(self, quality_threshold: float):
        """Sets the quality threshold to use for optimization  termination.
        Returns the optimizer for chaining setup calls (e.g. optimizer.with_dataset(x).start())"""
        self.set_quality_threshold(quality_threshold)
        return self

    def set_max_time(self, time_threshold: Union[datetime.timedelta, float,int]):
        """Sets the maximum allowed time since start for the last iteration to start.
         Accepts a timedelta or seconds."""
        if isinstance(time_threshold,datetime.timedelta):
            self.max_runtime = time_threshold
        elif isinstance(time_threshold,float) or isinstance(time_threshold,int):
            self.max_runtime = datetime.timedelta(seconds=time_threshold)
        else:
            raise ValueError("Wrong Max Time")

    def with_max_runtime(self, time_threshold: Union[datetime.timedelta, float]):
        """Sets the maximum allowed time since start for the last iteration to start.
        Accepts a timedelta or seconds.
        Returns the optimizer object for chaining calls."""
        self.set_max_time(time_threshold)
        return self

    def _create_optimizer(self):
        if self.optimization is None:
            raise ValueError("No pipeline was specified for optimization!")
        if self.data is None:
            raise ValueError("No data was specified for optimization!")
        self.allow_next_iteration = True
        if self.algorithm == AvailableAlgorithms.FixedRandomSearch:
            self.optimizer = FixedRandomSearch(self.optimization, self.data)
        elif self.algorithm == AvailableAlgorithms.Bayesian:
            self.optimizer = BayesianKernel(self.optimization, self.data)
        elif self.algorithm == AvailableAlgorithms.NelderMead:
            self.optimizer = NelderMead(self.optimization, self.data)
        elif self.algorithm == AvailableAlgorithms.SimulatedAnnealing:
            self.optimizer = SimulatedAnnealing(self.optimization, self.data)
            # for BPI16: ~250 Models / 30 sec = 8,3 m/s -> calculate k_max for optimal temperature curve
            # self.optimizer.k_max = self.max_runtime.seconds * 8.3
            self.optimizer.max_time = self.max_runtime # pass max runtime to adapt k_max / temperature
        else:
            raise NotImplementedError("The selected algorithm is not yet implemented")

    def start(self) -> datetime.timedelta:
        """Starts the optimizer synchronously. This may block the calling thread for a long time."""
        self._create_optimizer()
        # run a single worker
        self.start_time = datetime.datetime.now()
        self.parallel_worker(self.optimizer.get_workers(1)[0])
        return datetime.datetime.now() - self.start_time

    def start_stepwise(self):
        self._create_optimizer()
        self.worker = self.optimizer.get_workers(1)[0]

    def step(self):
        self.worker()
        self.iter_no += 1

    def parallel_worker(self, iteration: Callable):
        """Loops the iteration function as long as the optimizer should run."""
        while self.allow_next_iteration:
            # iterate
            iteration()
            self.iter_no += 1
            # terminate optimization if quality or runtime reached
            if self.optimizer.get_best_quality() >= self.quality_threshold or\
                    datetime.datetime.now()-self.start_time >= self.max_runtime or \
                    (self.iter_no > 5 and self.retrieve_full_history()["quality"][-5] ==
                    self.retrieve_full_history()["quality"][-4]==
                    self.retrieve_full_history()["quality"][-2]==
                    self.retrieve_full_history()["quality"][-2]==
                    self.retrieve_full_history()["quality"][-1]):
                self.allow_next_iteration = False

    def as_parallel_workers(self, worker_count: int = 16) -> List[Callable]:
        """Creates a list of Callables.
        Each item can be processed in parallel with any other item.
        To perform the optimization, call parallel_worker for every item in it's own thread."""
        self._create_optimizer()
        if not self.optimizer.is_parallel_allowed() and worker_count > 1:
            raise NotImplementedError("selected algorithm does not allow parallel execution")
        return self.optimizer.get_workers(worker_count)

    def get_current_runtime(self) -> datetime.timedelta:
        """Gets the current runtime of the optimizer."""
        return datetime.datetime.now() - self.start_time

    def stop(self):
        """Stops the optimizer gracefully by letting the current iteration complete."""
        self.allow_next_iteration = False

    def retrieve_best(self) -> pandas.DataFrame:
        """Retrieves the best configuration, result and quality as a pandas row"""
        return self.optimizer.get_best()

    def retrieve_full_history(self) -> pandas.DataFrame:
        """Retrieves the entire optimization history."""
        return self.optimizer.history

