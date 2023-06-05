from L03Discovery.Supported.Event import *
from enum import Enum


class EventFilterType(Enum):

	TimeContainment = TimeContainment
	BetweenFilter = BetweenFilter
	AttributeValue = AttributeValue
