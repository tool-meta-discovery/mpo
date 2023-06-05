from L02Parameter.Enumeration.ParameterType import ParameterType



""" this class is intended to be the super class for all other
parameter classes and provides the basic structure and some 
utility methods. Make sure to inherit from this class if you 
want to add your own parameter types. For more information on 
that, check out the doc string of the L02Parameter module. """



class ParameterSuperClass:

	def __init__(self,name,description,value_type):

		self.check_input_type(name,str)
		self.check_input_type(description,str)
		self.check_input_type(value_type,ParameterType)

		self.name = name
		self.description = description
		self.value_type = value_type
		self.current_value = None

	def check_input_type(self,input,required_type):
		if not isinstance(input, required_type):
			raise TypeError("Invalid Type For Parameter Attribute")

	def check_in_range(self, value, lower, upper):
		if not lower <= value <= upper:
			raise ValueError("Value Out Of Range")

	def check_in_list(self,value,possible_list):
		if not value in possible_list:
			raise ValueError("Value Not Possible")

	def check_in_dict(self,value,possible_dict):
		if not value in possible_dict:
			raise ValueError("Not In Dict")