from L02Parameter.Supported.ParameterSuperClass import ParameterSuperClass
from L02Parameter.Enumeration.ParameterType import ParameterType
import math



""" this class is intended to represent any numeric 
parameter and provides a lower and upper bound restriction 
that can be set. The bounds will be enforced when the current
value changes, and all changes beyond these borders will lead
to a value error exception. """



class ParameterNumeric(ParameterSuperClass):

	def __init__(self, name, description):
		super().__init__(name, description, ParameterType.Numeric)
		self.lower_range_end = -math.inf
		self.upper_range_end = math.inf
		self.current_value = 0

	def set_lower_range(self, new_lower_range_end):
		self.check_input_type(new_lower_range_end, float)
		self.check_in_range(self.current_value, new_lower_range_end, self.upper_range_end)
		self.lower_range_end = new_lower_range_end

	def set_upper_range(self, new_upper_range_end):
		self.check_input_type(new_upper_range_end, float)
		self.check_in_range(self.current_value, self.lower_range_end, new_upper_range_end)
		self.upper_range_end = new_upper_range_end

	def set_current_value(self, new_current_value):
		self.check_input_type(new_current_value, float)
		self.check_in_range(new_current_value, self.lower_range_end, self.upper_range_end)
		self.current_value = new_current_value

	def get_info_dict(self):
		return {"name":self.name,
				"description":self.description,
				"type":"numeric",
				"lower_bound":str(self.lower_range_end),
				"upper_bound":str(self.upper_range_end),
				"start_value":str(self.current_value),
		}

	def set_info_dict(self, info_dict):
		required_keys = ["lower_bound", "upper_bound", "start_value"]
		potential_errors = [self.check_in_dict(key, info_dict) for key in required_keys]
		self.set_current_value(float(info_dict["start_value"]))
		self.set_lower_range(float(info_dict["lower_bound"]))
		self.set_upper_range(float(info_dict["upper_bound"]))
