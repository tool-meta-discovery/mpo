from L03Discovery.Supported.Quality import *
from enum import Enum


class QualityMeasureType(Enum):

	PrecisionConformance = PrecisionConformance
	PrecisionAlignment = PrecisionAlignment
	ReplayFitnessToken = ReplayFitnessToken
	ReplayFitnessAlignment = ReplayFitnessAlignment
	GeneralizationToken = GeneralizationToken
	SimplicityArcDegree = SimplicityArcDegree