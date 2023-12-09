from enum import Enum


class ControlLogicSequencingPolicy(str, Enum):
    EDD = "EDD"
    FIFO = "FIFO"
    LIFO = "LIFO"
    ODD = "ODD"
    SPT = "SPT"

    def __str__(self) -> str:
        return str(self.value)
