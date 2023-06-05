from L02Parameter.Supported.ParameterSelection import *
from L02Parameter.Supported.ParameterTime import *
from L02Parameter.Supported.ParameterFixedValue import *
from L02Parameter.Supported.ParameterIntegral import *
from L02Parameter.Supported.ParameterNumeric import *

""" this module contains the different parameter classes
and their super class represent the parameters of the 
different steps in the discovery process. Each parameter
class needs to provide a current_value attribute and some
methods for setting the current values and control for any
restrictions upon them. Additionally every parameter needs 
to provide a get_info_dict method for displaying all it's
content in a comprehensible manner and a set_info_dict 
method to edit the content in the same way. """