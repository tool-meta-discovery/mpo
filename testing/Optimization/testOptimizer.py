from L03Discovery.Capsules.PipelineObject import PipelineObject
from L03Discovery.Capsules.DataSetObject import DataSetObject
from L02Parameter.Enumeration.ParameterType import ParameterType
from L03Discovery.Enumeration.QualityMeasureType import QualityMeasureType
from L03Discovery import *
import datetime
from pm4py.objects.petri_net.exporter.exporter import apply as export

from L04Optimization.Meta.AvailableAlgorithms import AvailableAlgorithms
from L04Optimization.Optimizer import Optimizer

"""Load a test data set"""
import pandas as pd
from pm4py.objects.log.util import dataframe_utils
from pm4py.objects.conversion.log import converter as log_converter

log_csv = pd.read_csv('../data/BPI2016_Complaints.csv', sep=';')
log_csv = dataframe_utils.convert_timestamp_columns_in_df(log_csv)
log_csv = log_csv.sort_values('ContactDate')
log_csv.rename(columns={'ComplaintTopic_EN': 'concept:name', 'ContactDate': 'time:timestamp'}, inplace=True)
parameters = {log_converter.Variants.TO_EVENT_LOG.value.Parameters.CASE_ID_KEY: 'CustomerID'}
log = log_converter.apply(log_csv, parameters=parameters)
capsule_object = DataSetObject(log)


""" Setup the pipeline object first, it will guide you through the 
full process of specifying everything needed for the optimization. """
pipeLineObject = PipelineObject()
pipeLineObject.init_on_data_set(capsule_object)
resulting_optimization_objects = pipeLineObject.get_optimization_objects()

k=0
for example_object in resulting_optimization_objects:
    """create an optimizer first"""
    optimizer = Optimizer()

    """To run the optimizer for an optimization object, we first need to configure it.
     This can be done using individual set methods or, as displayed here, in a more compact way."""
    optimizer.with_optimization(example_object).with_dataset(capsule_object)

    """The following settings are optional:"""
    optimizer.set_quality_threshold(0.99)
    variant = AvailableAlgorithms.NelderMead
    optimizer.set_algorithm(variant)
    optimizer.set_max_time(30)

    """The optimization can be run on the current thread with one worker using"""
    optimizer.start()
    """This blocks the current thread until the optimizer terminates.
    To avoid this, you can retrieve a list of callables and call each one using the parallel_worker function of the
    optimizer in parallel."""

    #callables = optimizer.as_parallel_workers()  # you can specify a number of workers to be created
    #for callable in callables:
    #    optimizer.parallel_worker(callable)

    """To terminate the optimization before reaching the quality threshold, you can call"""
    #optimizer.stop()

    """At any time you can retrieve the current best performing model, including quality and parameter settings as a row
    of a pandas DataFrame using"""
    df = optimizer.retrieve_best()
    import matplotlib.pyplot as plt
    hst = optimizer.retrieve_full_history()["quality"].reset_index().drop(columns=["index"])
    hst.plot()
    plt.title("Quality over iterations (k="+str(k)+")")
    net,im,fm = df["result"]
    export(net,im,"test"+str(k)+".pnml",fm)
    k+=1
    plt.show()
    print("test"+str(k)+".pnml:")
    print(df)
    if __debug__:
        if variant == AvailableAlgorithms.SimulatedAnnealing:
            temps = optimizer.optimizer.temps
            plt.plot(temps)
            plt.title("Temperature over iterations")
            plt.show()
            props = optimizer.optimizer.props
            plt.plot(props)
            plt.title("Probabilities over iterations")
            plt.show()
            de = optimizer.optimizer.delta_e
            plt.plot(de)
            plt.title("Energy difference over iterations")
            plt.show()
