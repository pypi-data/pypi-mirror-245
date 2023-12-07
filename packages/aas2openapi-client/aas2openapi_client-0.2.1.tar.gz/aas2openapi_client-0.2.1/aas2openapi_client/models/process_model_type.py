from enum import Enum


class ProcessModelType(str, Enum):
    GRAPH = "Graph"
    SEQUENTIAL = "Sequential"
    SINGLE = "Single"

    def __str__(self) -> str:
        return str(self.value)
