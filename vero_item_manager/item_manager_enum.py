from enum import Enum


class ItemState(Enum):
    STORE = 0
    NOT_STORE = 1

    def __str__(self):
        if self == ItemState.STORE:       return "Stored"
        elif self == ItemState.NOT_STORE: return "Not stored"


class ThresholdWeight(Enum):
    NAME = 2.0
    FEAT = 1.5
    DESC = 1.0
