from L04Optimization.Meta.AvailableAlgorithms import AvailableAlgorithms
from L04Optimization.Optimizer import Optimizer
"""This module contains functionality to iteratively optimize a set of parameters for optimal model quality. The 
parameters and target quality measures are submitted to an Optimizer object together with the data for model 
generation, maximum runtime, quality threshold and selected optimization algorithm. 

Apart from the Optimizer object it contains the enumeration AvailableAlgorithms containing all currently possible 
optimization methods. The implementations of the different methods are accessed through the Optimizer object and do 
not need to be imported. If you want to look at the implementation details, take a look at the classes inside the 
'Implementations' package."""