import unittest
import L03Discovery
from L03Discovery.Enumeration import *

# Unit Tests for Pipeline Object
class tests_L03_PipelineObject(unittest.TestCase):

    # dictionary
    def test_PipelineObject_checkdict(self):
        pipeline_obj = L03Discovery.PipelineObject()
        dict = {'asd': 123, 'tyu': '456'}
        with self.assertRaises(ValueError):
            pipeline_obj.check_in_dict('qwe', dict)

    def test_PipelineObject_removelist_empty(self):
        pipeline_obj = L03Discovery.PipelineObject()
        dict = {'asd': 123, 'tyu': '456'}
        pipeline_obj.remove_list_from_dict(['asd', 'tyu'], dict)
        self.assertEqual(dict, {})
    def test_PipelineObject_removelist_missing(self):
        pipeline_obj = L03Discovery.PipelineObject()
        dict = {'asd': 123, 'tyu': '456'}
        with self.assertRaises(ValueError):
            pipeline_obj.remove_list_from_dict(['123', 'tyu'], dict)
    def test_PipelineObject_removelist_notdict(self):
        pipeline_obj = L03Discovery.PipelineObject()
        dict = '123'
        with self.assertRaises(AttributeError):
            pipeline_obj.remove_list_from_dict(['123', 'tyu'], dict)

    def test_PipelineObject_removevalue_empty(self):
        pipeline_obj = L03Discovery.PipelineObject()
        dict = {'asd': 123, 'tyu': '456'}
        pipeline_obj.remove_value_from_dict('tyu', dict)
        pipeline_obj.remove_value_from_dict('asd', dict)
        self.assertEqual(dict, {})
    def test_PipelineObject_removevalue_missing(self):
        pipeline_obj = L03Discovery.PipelineObject()
        dict = {'asd': 123, 'tyu': '456'}
        with self.assertRaises(ValueError):
            pipeline_obj.remove_value_from_dict('123', dict)
    def test_PipelineObject_removevalue_notdict(self):
        pipeline_obj = L03Discovery.PipelineObject()
        dict = '123'
        with self.assertRaises(AttributeError):
            pipeline_obj.remove_value_from_dict('123', dict)

    # algorithm functions
    def test_PipelineObject_reset_algo(self):
        pipeline_obj = L03Discovery.PipelineObject()
        old_info_list = pipeline_obj.get_algo_info_list()
        new_info_list = [old_info_list[0]]
        pipeline_obj.set_algo_info_list(new_info_list)
        pipeline_obj.reset_algorithm()
        self.assertEqual(old_info_list, pipeline_obj.get_algo_info_list())

    def test_PipelineObject_set_algo_equal(self):
        pipeline_obj = L03Discovery.PipelineObject()
        info_list = pipeline_obj.get_algo_info_list()
        new = [info_list[0]]
        pipeline_obj.set_algo_info_list(new)
        self.assertEqual(new, pipeline_obj.get_algo_info_list())
    def test_PipelineObject_set_algo_string(self):
        pipeline_obj = L03Discovery.PipelineObject()
        with self.assertRaises(TypeError):
            pipeline_obj.set_algo_info_list(['qweqwe', 'qweqweqwe'])
    def test_PipelineObject_set_algo_dict(self):
        pipeline_obj = L03Discovery.PipelineObject()
        with self.assertRaises(KeyError):
            pipeline_obj.set_algo_info_list([{'qwe': 'qwe'}])

    def test_PipelineObject_unselect_algo_empty(self):
        pipeline_obj = L03Discovery.PipelineObject()
        pipeline_obj.unselect_algorithm([AlgorithmType.InductiveMiner, AlgorithmType.InductiveMinerD,
                                         AlgorithmType.AlphaMiner, AlgorithmType.InductiveMinerF,
                                         AlgorithmType.HeuristicMiner])
        self.assertEqual([], pipeline_obj.get_algo_info_list())
    def test_PipelineObject_unselect_algo_type(self): # sollte ein anderer fehler kommen
        pipeline_obj = L03Discovery.PipelineObject()
        with self.assertRaises(ValueError):
            pipeline_obj.unselect_algorithm({'bla'})
    def test_PipelineObject_unselect_algo_value(self):
        pipeline_obj = L03Discovery.PipelineObject()
        pipeline_obj.unselect_algorithm([AlgorithmType.InductiveMiner])
        with self.assertRaises(ValueError):
            pipeline_obj.unselect_algorithm([AlgorithmType.InductiveMiner])

    # event filter
    def test_PipelineObject_reset_event(self):
        pipeline_obj = L03Discovery.PipelineObject()
        old_info_list = pipeline_obj.get_event_info_list()
        new_info_list = [old_info_list[0]] # todo
        pipeline_obj.set_event_info_list(new_info_list)
        pipeline_obj.reset_event_filter()
        self.assertEqual(old_info_list, pipeline_obj.get_event_info_list())
    def test_PipelineObject_set_event_equal(self):
        pipeline_obj = L03Discovery.PipelineObject()
        info_list = pipeline_obj.get_event_info_list()
        new = [info_list[0]]
        pipeline_obj.set_event_info_list(new)
        self.assertEqual(new, pipeline_obj.get_event_info_list())
    def test_PipelineObject_set_event_string(self):
        pipeline_obj = L03Discovery.PipelineObject()
        with self.assertRaises(TypeError):
            pipeline_obj.set_event_info_list(['qweqwe', 'qweqweqwe'])
    def test_PipelineObject_set_event_dict(self):
        pipeline_obj = L03Discovery.PipelineObject()
        with self.assertRaises(KeyError):
            pipeline_obj.set_event_info_list([{'qwe': 'qwe'}])

    def test_PipelineObject_unselect_event_empty(self): # datetime?
        pipeline_obj = L03Discovery.PipelineObject()
        pipeline_obj.unselect_event_filter([EventFilterType.TimeContainment,
                                            EventFilterType.BetweenFilter,
                                            EventFilterType.AttributeValue])
        self.assertEqual([], pipeline_obj.get_event_info_list())
    def test_PipelineObject_unselect_event_type(self):
        pipeline_obj = L03Discovery.PipelineObject()
        with self.assertRaises(ValueError):
            pipeline_obj.unselect_event_filter({'bla'})
    def test_PipelineObject_unselect_event_value(self):
        pipeline_obj = L03Discovery.PipelineObject()
        pipeline_obj.unselect_event_filter([EventFilterType.TimeContainment])
        with self.assertRaises(ValueError):
            pipeline_obj.unselect_event_filter([EventFilterType.TimeContainment])

    # trace filter
    def test_PipelineObject_reset_trace(self):
        pipeline_obj = L03Discovery.PipelineObject()
        old_info_list = pipeline_obj.get_trace_info_list()
        new_info_list = [old_info_list[0]]
        pipeline_obj.set_trace_info_list(new_info_list)
        pipeline_obj.reset_trace_filter()
        self.assertEqual(old_info_list, pipeline_obj.get_trace_info_list())

    def test_PipelineObject_set_trace_equal(self):
        pipeline_obj = L03Discovery.PipelineObject()
        info_list = pipeline_obj.get_trace_info_list()
        new = [info_list[0]]
        pipeline_obj.set_trace_info_list(new)
        self.assertEqual(new, pipeline_obj.get_trace_info_list())
    def test_PipelineObject_set_trace_string(self):
        pipeline_obj = L03Discovery.PipelineObject()
        with self.assertRaises(TypeError):
            pipeline_obj.set_trace_info_list(['qweqwe', 'qweqweqwe'])
    def test_PipelineObject_set_trace_dict(self):
        pipeline_obj = L03Discovery.PipelineObject()
        with self.assertRaises(KeyError):
            pipeline_obj.set_trace_info_list([{'qwe': 'qwe'}])

    def test_PipelineObject_unselect_trace_empty(self):
        pipeline_obj = L03Discovery.PipelineObject()
        pipeline_obj.unselect_trace_filter([TraceFilterType.TimeContainment,
                                            TraceFilterType.TimeIntersection,
                                            TraceFilterType.CaseSize,
                                            TraceFilterType.EndActivity,
                                            TraceFilterType.FrequentVariants,
                                            TraceFilterType.StartActivity])
        self.assertEqual([], pipeline_obj.get_trace_info_list())
    def test_PipelineObject_unselect_trace_type(self):
        pipeline_obj = L03Discovery.PipelineObject()
        with self.assertRaises(ValueError):
            pipeline_obj.unselect_trace_filter({'bla'})
    def test_PipelineObject_unselect_trace_value(self):
        pipeline_obj = L03Discovery.PipelineObject()
        pipeline_obj.unselect_trace_filter([TraceFilterType.TimeContainment])
        with self.assertRaises(ValueError):
            pipeline_obj.unselect_trace_filter([TraceFilterType.TimeContainment])

    # quality measures
    def test_PipelineObject_reset_quality(self):
        pipeline_obj = L03Discovery.PipelineObject()
        old_info_list = pipeline_obj.get_quality_info_list()
        new_info_list = [old_info_list[0]]
        pipeline_obj.set_quality_info_list(new_info_list)
        pipeline_obj.reset_quality()
        self.assertEqual(old_info_list, pipeline_obj.get_quality_info_list())
    def test_PipelineObject_set_quality_equal(self):
        pipeline_obj = L03Discovery.PipelineObject()
        info_list = pipeline_obj.get_quality_info_list()
        new = [info_list[0]]
        pipeline_obj.set_quality_info_list(new)
        self.assertEqual(new, pipeline_obj.get_quality_info_list())
    def test_PipelineObject_set_quality_string(self):
        pipeline_obj = L03Discovery.PipelineObject()
        with self.assertRaises(TypeError):
            pipeline_obj.set_quality_info_list(['qweqwe', 'qweqweqwe'])
    def test_PipelineObject_set_quality_dict(self):
        pipeline_obj = L03Discovery.PipelineObject()
        with self.assertRaises(KeyError):
            pipeline_obj.set_quality_info_list([{'qwe': 'qwe'}])

    def test_PipelineObject_unselect_quality_empty(self):
        pipeline_obj = L03Discovery.PipelineObject()
        pipeline_obj.unselect_quality_measure([QualityMeasureType.PrecisionAlignment, QualityMeasureType.ReplayFitnessAlignment,
                                       QualityMeasureType.SimplicityArcDegree, QualityMeasureType.GeneralizationToken,
                                       QualityMeasureType.ReplayFitnessToken, QualityMeasureType.PrecisionConformance])
        self.assertEqual([], pipeline_obj.get_quality_info_list())
    def test_PipelineObject_unselect_quality_type(self):
        pipeline_obj = L03Discovery.PipelineObject()
        with self.assertRaises(ValueError):
            pipeline_obj.unselect_quality_measure({'bla'})
    def test_PipelineObject_unselect_quality_value(self):
        pipeline_obj = L03Discovery.PipelineObject()
        pipeline_obj.unselect_quality_measure([QualityMeasureType.PrecisionAlignment])
        with self.assertRaises(ValueError):
            pipeline_obj.unselect_quality_measure([QualityMeasureType.PrecisionAlignment])

# Run all Tests
if __name__ == '__main__':
    unittest.main()