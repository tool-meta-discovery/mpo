from L02Parameter.Supported.ParameterSuperClass import ParameterSuperClass
from L02Parameter.Enumeration.ParameterType import ParameterType



""" this class is intended for internal usage only and 
can be used if you, as a developer, want to (or need to) 
hard code a parameter for any of the process discovery steps. 
All other modules will not edit the content of an instance
of this class and just use the hard coded constant value. """



class ParameterFixedValue(ParameterSuperClass):

	def __init__(self, name, description, constant_value):
		super().__init__(name, description, ParameterType.FixedValue)
		self.current_value = constant_value

