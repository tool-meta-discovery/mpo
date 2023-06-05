from L03Discovery import *
from L04Optimization.Optimizer import *
from L04Optimization.Meta.AvailableAlgorithms import AvailableAlgorithms
from L05Parallelization.ParallelProcessor import ParallelProcessor


class ParallelLauncher:
    """This class is designed as an interface for starting a (parallelized) optimization process."""

    def __init__(self, pipe: PipelineObject,
                 data: DataSetObject,
                 result: ResultObject,
                 time: datetime.timedelta, kernel=AvailableAlgorithms.NelderMead,abort_check=None):
        self.pipe,self.data,self.result,self.time,self.kernel = pipe,data,result,time,kernel
        self.processor = ParallelProcessor().with_data(data).with_pipeline(pipe).with_max_time(time) \
            .with_optimizer_algorithm(kernel).with_result_object(result).with_abort_check(abort_check)

    def start(self) -> bool:
        """Starts the execution in parallel."""
        try:
            return self.processor.execute_optimization_parallel()
        except BaseException as ex:
            print("Generic parallelization error: " + str(ex))
            self.processor.result_object.set_error("Generic parallelization error!")
            return False

    def alternative_start(self):
        """Starts the execution not parallel."""
        for op in self.pipe.get_optimization_objects():
            task = Optimizer().with_optimization(op).with_dataset(self.data).with_algorithm(self.kernel)
            task.with_max_runtime(self.time/len(self.pipe.get_optimization_objects())).start()
            self.result.histories.append(task.retrieve_full_history())
            self.result.store_changes()