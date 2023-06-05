import types
import pickle

class DiscoveryStepSuperClass:

	def __init__(self,name,description,method_callable):

		self.check_input_type(name,str)
		self.check_input_type(description,str)
		self.check_input_type(method_callable,types.FunctionType)
		self.name = name
		self.description = description
		self.method_callable = method_callable
		self.parameter_list = []

	def check_input_type(self,input,required_type):
		if not isinstance(input, required_type):
			raise ValueError("Invalid Type")

	def check_in_list(self,value,possible_list):
		if not value in possible_list:
			raise ValueError("Not In List")

	def get_all_parameter_names(self):
		return [parameter.name for parameter in self.parameter_list]

	def get_all_parameter_descriptions(self):
		return [parameter.description for parameter in self.parameter_list]

	def get_all_parameter_types(self):
		return [parameter.value_type for parameter in self.parameter_list]

	def get_all_parameter_current_values(self):
		return [parameter.current_value for parameter in self.parameter_list]

	def get_one_parameter(self,parameter_name):
		self.check_in_list(parameter_name,self.get_all_parameter_names())
		for parameter in self.parameter_list:
			if parameter.name == parameter_name:
				return parameter

	def execute_on_dataset(self,data_set):
		arguments = [data_set.dataframe] + (self.get_all_parameter_current_values())
		return self.method_callable(*arguments)

	def dumps(self):
		self.parameter_list = [pickle.dumps(parameter) for parameter in self.parameter_list]
		pickled_step_object = pickle.dumps(self)
		self.parameter_list = [pickle.loads(parameter) for parameter in self.parameter_list]
		return pickled_step_object

	def loads(self,pickled_step_object):
		step_object = pickle.loads(pickled_step_object)
		step_object.parameter_list = [pickle.loads(parameter) for parameter in step_object.parameter_list]
		return step_object

	def get_deep_copy(self):
		return self.loads(self.dumps())

	def get_info_dict(self):
		return {
			"name":self.name,
			"description":self.description,
			"parameters":[parameter.get_info_dict() for parameter in self.parameter_list]
		}

	def set_info_dict(self,new_info_dict):
		parameter_dict_old = {parameter.name: parameter for parameter in self.parameter_list}
		parameter_dict_new = {parameter["name"]: parameter for parameter in new_info_dict["parameters"]}
		for name,setting in parameter_dict_new.items():
			if name in parameter_dict_old:
				parameter_dict_old[name].set_info_dict(setting)

	def init_on_data_set(self,data_set_object):
		pass
