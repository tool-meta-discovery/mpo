from L05Parallelization.ParallelProcessor import ParallelProcessor
from L05Parallelization.ParallelLauncher import ParallelLauncher

"""This package contains functionality to parallelize the optimization of multiple parameter sets. To perform 
optimization for all possible filter/discovery combinations simultaneously in parallel you can submit your 
PipelineObject, DataSetObject, a maximum runtime, one of the available optimization algorithms and a target ResultObject
to a ParallelLauncher object. To start the execution you then can call start() on said object, which blocks execution 
until the ParallelProcessor used internally by the ParallelLauncher terminates.

Apart from the ParallelLauncher object you could also create a ParallelProcessor object and use some more configuration 
options. The ParallelProcessor object runs until the maximum runtime is passed or the quality threshold was achieved for
one of the different combinations. It iteratively runs one iteration of each combination in parallel before saving the 
results to the ResultObject and continuing with the next set of iterations. By default the ParallelProcessor uses a 
number of workers equal to your CPU count, or 4 if that count is not available."""
