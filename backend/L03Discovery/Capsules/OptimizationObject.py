

class OptimizationObject:

	def __init__(self,event_filter_list,trace_filter_list,algorithm,quality_measure_list):

		if None in event_filter_list:
			event_filter_list.remove(None)
		if None in trace_filter_list:
			trace_filter_list.remove(None)
		self.event_filter_list = event_filter_list
		self.trace_filter_list = trace_filter_list
		self.algorithm = algorithm
		self.quality_measure_list = quality_measure_list

	def execute_on_dataset(self,dataset):

		for event_filter in self.event_filter_list:
			if event_filter:
				dataset.dataframe = event_filter.execute_on_dataset(dataset)
		for trace_filter in self.trace_filter_list:
			if trace_filter:
				dataset.dataframe = trace_filter.execute_on_dataset(dataset)
		dataset.result = self.algorithm.execute_on_dataset(dataset)
		score_list = []
		score_dict = {}
		for measure in self.quality_measure_list:
			try:
				score = measure.execute_on_dataset(dataset)
				try:
					if len(dataset.result[0].places) <= 2:
						score = 0
				except:
					pass
			except:
				score = 0.0
			score_list.append(score)
			score_dict[measure.name] = score

		dataset.score = sum(score_list, 0)/len(score_list)
		try:
			if len(dataset.result[0].places) <= 2:
				dataset.score = 0
		except:
			pass
		dataset.dataframe = dataset.original_data
		score_dict["overall"] = dataset.score
		dataset.score_dict = score_dict

		print(dataset.score)
		print(score_dict)

