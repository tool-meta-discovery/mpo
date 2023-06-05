from L02Parameter.Supported.ParameterSuperClass import ParameterSuperClass
from L02Parameter.Enumeration.ParameterType import ParameterType



""" this class is intended to represent any selection 
parameter and provides the restriction that the current 
value has to be included in a given set of possible options
The restriction will be enforced when the current value changes,
and all changes to a value not included in the given option set
will lead to a value error. Please note, that all entries in this
option set have to provide pickle support. If you want to include
some options that do not provide native pickle support, consider
overwriting the internal __setstate__ and __getstate__ methods """



class ParameterSelection(ParameterSuperClass):

	def __init__(self, name, description):
		super().__init__(name, description, ParameterType.Selection)
		self.selection_set = []
		self.current_value = None

	def get_selection_set(self):
		return self.selection_set

	def set_selection_set(self,new_selection_set):
		self.check_input_type(new_selection_set,list)
		self.selection_set = new_selection_set

	def set_current_value(self, new_current_value):
		self.check_in_list(new_current_value,self.selection_set)
		self.current_value = new_current_value

	def get_info_dict(self):
		return {"name":self.name,
				"description":self.description,
				"type":"selection",
				"selection_set":[str(entry) for entry in self.selection_set],
				"start_value":str(self.current_value),
		}

	def set_info_dict(self, info_dict):
		required_keys = ["selection_set", "start_value"]
		potential_errors = [self.check_in_dict(key, info_dict) for key in required_keys]
		new_set = []
		for new in info_dict["selection_set"]:
			for old in self.selection_set:
				if str(old) == new:
					new_set.append(old)
		self.set_selection_set(new_set)
		for old in self.selection_set:
			if str(old) == info_dict["start_value"]:
				self.set_current_value(old)

