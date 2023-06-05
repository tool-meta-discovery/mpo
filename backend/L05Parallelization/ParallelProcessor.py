import datetime
from typing import List, Optional, Callable, Tuple
from multiprocessing import Pool

import os

import pandas
from numpy import argmax

from L03Discovery import ResultObject
from L04Optimization.Meta.AvailableAlgorithms import AvailableAlgorithms
from L03Discovery.Capsules.DataSetObject import DataSetObject
from L03Discovery.Capsules.OptimizationObject import OptimizationObject
from L03Discovery.Capsules.PipelineObject import PipelineObject
from L04Optimization.Optimizer import Optimizer


class ParallelProcessor:
    """This class implements functionality to handle parallel execution of optimizations.
    with each iteration of it's internal loop if runs one iteration for each optimization object."""
    pipeline: PipelineObject
    quality_threshold: float
    max_num_workers: int
    max_overall_time: datetime.timedelta
    workers: Pool
    data: DataSetObject
    optimizer_algorithm: AvailableAlgorithms
    onIterationComplete: Optional[Callable]
    result_object: ResultObject

    def __init__(self):
        self.optimizers = list()
        cpus = os.cpu_count()
        if cpus is not None:
            self.max_num_workers = int(cpus / 2)
        else:
            self.max_num_workers = 4
        self.quality_threshold = 1
        self.max_overall_time = datetime.timedelta(minutes=5)
        self.optimizer_algorithm = AvailableAlgorithms.NelderMead
        self.abort_check = None
        self.all_skipped = False

    def set_pipeline(self, pipeline: PipelineObject):
        """Sets the pipeline object to derive the OptimizationObjects from."""
        self.pipeline = pipeline

    def with_pipeline(self, pipeline: PipelineObject):
        """Sets the pipeline object to derive the OptimizationObjects from and returns the ParallelProcessor for
        chaining. """
        self.set_pipeline(pipeline)
        return self

    def set_data(self, data: DataSetObject):
        """Sets the data to optimize the model for. """
        self.data = data

    def with_data(self, data: DataSetObject):
        """Sets the data to optimize for and returns the ParallelProcessor for
        chaining. """
        self.set_data(data)
        return self

    def set_quality_threshold(self, quality_threshold: float):
        """Sets the quality score threshold for early termination. """
        self.quality_threshold = quality_threshold

    def with_quality_threshold(self, quality_threshold: float):
        """Sets the quality score threshold for early termination and returns the ParallelProcessor for chaining. """
        self.set_quality_threshold(quality_threshold)
        return self

    def set_max_time(self, time: datetime.timedelta):
        """Sets the runtime threshold for early termination. """
        self.max_overall_time = time

    def with_max_time(self, time: datetime.timedelta):
        """Sets the runtime threshold for early termination and returns the ParallelProcessor for chaining. """
        self.set_max_time(time)
        return self

    def set_max_worker_count(self, worker_count: int):
        """Sets maximum number of parallel workers."""
        self.max_num_workers = worker_count

    def with_max_worker_count(self, worker_count: int):
        """Sets maximum number of parallel workers and returns the ParallelProcessor for chaining."""
        self.set_max_worker_count(worker_count)
        return self

    def set_abort_check(self, check_method):
        """Sets a callback to check for external early termination requests."""
        self.abort_check = check_method

    def with_abort_check(self, check_method):
        """Sets a callback to check for external early termination requests and returns the ParallelProcessor for
        chaining. """
        self.abort_check = check_method
        return self

    def set_optimizer_algorithm(self, optimizer_algorithm: AvailableAlgorithms):
        """Sets the optimization algorithm to be used."""
        self.optimizer_algorithm = optimizer_algorithm

    def with_optimizer_algorithm(self, optimizer_algorithm: AvailableAlgorithms):
        """Sets the optimization algorithm to be used and returns the ParallelProcessor for chaining."""
        self.set_optimizer_algorithm(optimizer_algorithm)
        return self

    def set_result_object(self, result_object: ResultObject):
        """Sets theResultObject to write results to."""
        self.result_object = result_object

    def with_result_object(self, result_object: ResultObject):
        """Sets theResultObject to write results to and returns the ParallelProcessor for chaining."""
        self.set_result_object(result_object)
        return self

    def kill_execution(self):
        """Kills the current execution. IMPORTANT: This may not get you any result!"""
        self.workers.terminate()
        self.result_object.finished = True
        self.result_object.store_changes()

    @classmethod
    def parallel_step(cls, res: Tuple[Optimizer, int]) -> Tuple[Optimizer, int, bool]:
        """gets called for each iteration for each optimization"""
        (optimizer, idx) = res  # extract parameters
        skipped = optimizer.iter_no > 5 and len(optimizer.retrieve_full_history()["quality"]) > 5  # enough data to
        # determine skipping?
        try:
            if skipped:
                skipped &= optimizer.retrieve_full_history().tail(5).std(ddof=0)["quality"] == 0  # skip if no change
        except:
            print("THAT Key error")
            skipped = False
        if not skipped:
            print("stepping" + str(idx))
            optimizer.step()  # perform one iteration of one optimizer
        else:
            print("skipping" + str(idx))
        return optimizer, idx, skipped

    def worker_callback(self, result: Tuple[Optimizer, int, bool]):
        """gets called for each optimizer after optimizations have completed one iteration"""
        try:
            print("callback for " + str(result[1]))
            self.all_skipped &= result[2]  # remember for early termination
            # extract parameters
            optimizer = result[0]
            i = result[1]
            # retrieve history for calculations
            hist = optimizer.retrieve_full_history()
        except BaseException as ex:
            print("Callback parameter unwrapping failed: " + str(ex))
            self.result_object.set_error("Callback parameter unwrapping failed!")
            return False
        try:
            max_q = argmax(hist.quality)  # highest quality in this optimizer
            self.result_object.histories[i] = hist  # remember history for this optimizer
            if self.result_object.argmax == (-1, -1):  # if there was no best model yet
                self.result_object.argmax = (i, max_q)  # this is the best one
            if hist.iloc[max_q, 0] >= self.result_object.histories[self.result_object.argmax[0]] \
                    .iloc[self.result_object.argmax[1], 0]:  # if the best model of this optimizer is the overall best
                self.result_object.argmax = (i, max_q)  # store new best model location
            if hist.iloc[max_q, 0] >= self.quality_threshold:  # if the best model is better than the threshold
                self.result_object.finished = True  # stop the optimizer
            self.result_object.store_changes()  # notify frontend
        except BaseException as ex:
            print("Callback result handling failed: " + str(ex))
            self.result_object.set_error("Callback result handling failed!")
            return False

    def execute_optimization_parallel(self):
        """Runs optimizers for each possible optimization object in parallel.
        Returns an awaiter object to wait for the execution of all optimizations.
        """
        try:
            # create optimization object list
            opt_objects: List[OptimizationObject] = self.pipeline.get_optimization_objects()
            if len(opt_objects) == 0:
                self.result_object.finished = True
                self.result_object.store_changes()
                return
        except BaseException as ex:
            print("Optimization retrieval failed: "+str(ex))
            self.result_object.set_error("Optimization retrieval failed!")
            return False
        try:
            # set up result object and optimizers
            self.result_object.histories = [pandas.DataFrame() for i in range(len(opt_objects))]  # list of correct length
            worker_count = min(self.max_num_workers, len(opt_objects))
            # setup workers
            for opt_object in opt_objects:
                optimizer = Optimizer()
                self.optimizers.append(optimizer)
                # set up and run optimizer
                optimizer.with_optimization(opt_object).with_quality_threshold(1).with_dataset(self.data) \
                    .with_algorithm(self.optimizer_algorithm).start_stepwise()
        except BaseException as ex:
            print("Optimizer creation failed: "+str(ex))
            self.result_object.set_error("Optimizer creation failed!")
            return False
        start_time = datetime.datetime.now()

        try:
            with Pool(worker_count) as self.workers:
                # check for timeout and other completion indicators
                while datetime.datetime.now() - start_time < self.max_overall_time and not self.result_object.finished \
                        and not self.all_skipped:
                    self.all_skipped = True
                    # chunk the optimizations
                    csize = min(len(self.optimizers), 16)
                    for i in range(0, len(self.optimizers), csize):
                        # check termination again
                        if self.abort_check and self.abort_check():
                            print("Job Aborted")
                            break
                        if datetime.datetime.now() - start_time >= self.max_overall_time:
                            print("Job timed out!")
                            break
                        print("iterating " + str(i) + " to " + str(min(i + csize, len(self.optimizers))))
                        try:
                            # start parallel processing of current chunk
                            results = self.workers.imap_unordered(ParallelProcessor.parallel_step,
                                                                  [(self.optimizers[i], i) for i in
                                                                   range(i, min(i + csize, len(self.optimizers)))],
                                                                  chunksize=int(csize /
                                                                                worker_count))
                            for res in results:
                                self.worker_callback(res)
                                self.optimizers[res[1]] = res[0]
                        except BaseException as ex:
                            print("Minibatch failed: " + str(ex))
                            self.result_object.set_error("Minibatch failed!")
                            return False

                    print("Iteration Finished ")
                try:
                    # upon termination of loop update result object
                    self.result_object.finished = True
                    self.result_object.store_changes()
                    # and clean up
                    self.workers.close()
                    self.workers.join()
                except BaseException as ex:
                    print("Multiprocessing cleanup failed: " + str(ex))
                    self.result_object.set_error("Multiprocessing cleanup failed!")
                    return False

        except BaseException as ex:
            print("Multiprocessing error: "+str(ex))
            self.result_object.set_error("Multiprocessing error!")
            return False

        return True

    def __getstate__(self):
        self_dict = self.__dict__.copy()
        if "workers" in self_dict:
            del self_dict['workers']
        return self_dict

    def __setstate__(self, state):
        self.__dict__.update(state)
