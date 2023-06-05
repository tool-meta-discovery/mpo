from L03Discovery.Enumeration import *
from L03Discovery.Capsules.OptimizationObject import OptimizationObject
from itertools import chain, combinations


class PipelineObject:

	def __init__(self):

		self.event_filter = self.get_available_event_filter()
		self.trace_filter = self.get_available_trace_filter()
		self.algorithm = self.get_available_algorithm()
		self.quality_measure = self.get_available_quality_measure()

	def check_in_dict(self,value,dictionary):
		if not value in dictionary.keys():
			raise ValueError("Invalid Type")

	def remove_value_from_dict(self,value,dictionary):
		self.check_in_dict(value,dictionary)
		dictionary.pop(value)

	def remove_list_from_dict(self,value_list,dictionary):
		for value in value_list:
			self.check_in_dict(value,dictionary)
			self.remove_value_from_dict(value,dictionary)

	def get_available_event_filter(self):
		return {enum:enum.value() for enum in EventFilterType}

	def get_available_trace_filter(self):
		return {enum:enum.value() for enum in TraceFilterType}

	def get_available_algorithm(self):
		return {enum:enum.value() for enum in AlgorithmType}

	def get_available_quality_measure(self):
		return {enum:enum.value() for enum in QualityMeasureType}



	def unselect_event_filter(self,event_filter_type_list):
		self.remove_list_from_dict(event_filter_type_list,self.event_filter)

	def unselect_trace_filter(self,trace_filter_type_list):
		self.remove_list_from_dict(trace_filter_type_list,self.trace_filter)

	def unselect_algorithm(self,algorithm_type_list):
		self.remove_list_from_dict(algorithm_type_list,self.algorithm)

	def unselect_quality_measure(self,quality_measure_type_list):
		self.remove_list_from_dict(quality_measure_type_list,self.quality_measure)



	def get_selected_event_filter(self):
		return self.event_filter

	def get_selected_trace_filter(self):
		return self.trace_filter

	def get_selected_algorithm(self):
		return self.algorithm

	def get_selected_quality_measure(self):
		return self.quality_measure



	def reset_event_filter(self):
		self.event_filter = self.get_available_event_filter()

	def reset_trace_filter(self):
		self.trace_filter = self.get_available_trace_filter()

	def reset_algorithm(self):
		self.algorithm = self.get_available_algorithm()

	def reset_quality(self):
		self.quality_measure = self.get_available_quality_measure()

	def get_event_info_list(self):
		return [entry.get_info_dict() for key,entry in self.event_filter.items()]

	def get_trace_info_list(self):
		return [entry.get_info_dict() for key,entry in self.trace_filter.items()]

	def get_algo_info_list(self):
		return [entry.get_info_dict() for key,entry in self.algorithm.items()]

	def get_quality_info_list(self):
		return [entry.get_info_dict() for key,entry in self.quality_measure.items()]

	def set_info_list(self,new_info_list,target):
		dict_old = {entry.name: entry for entry in target}
		dict_new = {entry["name"]: entry for entry in new_info_list}
		for name, setting in dict_new.items():
			if name in dict_old: dict_old[name].set_info_dict(setting)
		return {key: value for key, value in target.items() if value.name in list(dict_new.keys())}

	def set_event_info_list(self,new_info_list):
		self.event_filter = self.set_info_list(new_info_list,self.event_filter)

	def set_trace_info_list(self,new_info_list):
		self.trace_filter = self.set_info_list(new_info_list,self.trace_filter)

	def set_algo_info_list(self,new_info_list):
		self.algorithm = self.set_info_list(new_info_list,self.algorithm)

	def set_quality_info_list(self,new_info_list):
		self.quality_measure = self.set_info_list(new_info_list,self.quality_measure)

	def init_on_data_set(self,data_set_object):
		for name,filter in self.event_filter.items():filter.init_on_data_set(data_set_object)
		for name,filter in self.trace_filter.items():filter.init_on_data_set(data_set_object)
		for name,algorithm in self.algorithm.items():algorithm.init_on_data_set(data_set_object)
		for name,quality in self.quality_measure.items():quality.init_on_data_set(data_set_object)

	def get_optimization_objects(self):

		result = []
		event_filter_list = [value for key,value in self.event_filter.items()]
		trace_filter_list = [value for key,value in self.trace_filter.items()]
		algorithm_list = [value for key,value in self.algorithm.items()]
		quality_list = [value for key,value in self.quality_measure.items()]

		event_filter_list.append(None)
		trace_filter_list.append(None)

		event_filter_subset = list(chain.from_iterable(
			combinations(list(event_filter_list), length) for length in range(0, len(event_filter_list) + 1)))
		trace_filter_subset = list(chain.from_iterable(
			combinations(list(trace_filter_list), length) for length in range(0, len(trace_filter_list) + 1)))
		full_mode = False

		if full_mode:
			for event_set in event_filter_subset:
				for trace_set in trace_filter_subset:
					for algorithm in algorithm_list:
						result.append(OptimizationObject(event_set,trace_set,algorithm,quality_list))
		else:
			for event_filter in event_filter_list:
				for trace_filter in trace_filter_list:
					for algorithm in algorithm_list:
						result.append(OptimizationObject([event_filter], [trace_filter], algorithm, quality_list))
		print("Amount Of Optimization Objects "+str(len(result)))
		return result










