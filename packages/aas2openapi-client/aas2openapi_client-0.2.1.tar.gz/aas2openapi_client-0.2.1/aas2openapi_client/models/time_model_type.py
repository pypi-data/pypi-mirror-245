from enum import Enum


class TimeModelType(str, Enum):
    DISTANCE_BASED = "distance_based"
    DISTRIBUTION = "distribution"
    SEQUENTIAL = "sequential"

    def __str__(self) -> str:
        return str(self.value)
