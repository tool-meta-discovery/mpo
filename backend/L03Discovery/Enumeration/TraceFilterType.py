from L03Discovery.Supported.Trace import *
from enum import Enum


class TraceFilterType(Enum):
	TimeContainment = TimeContainment
	TimeIntersection = TimeIntersection
	CaseSize = CaseSize
	StartActivity = StartActivity
	EndActivity = EndActivity
	FrequentVariants = FrequentVariants