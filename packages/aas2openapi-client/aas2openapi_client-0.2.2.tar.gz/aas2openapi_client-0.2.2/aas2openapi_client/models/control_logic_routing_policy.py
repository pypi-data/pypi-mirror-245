from enum import Enum


class ControlLogicRoutingPolicy(str, Enum):
    ALTERNATING = "alternating"
    NEAREST = "nearest"
    RANDOM = "random"
    ROUND_ROBIN = "round_robin"
    SHORTEST_QUEUE = "shortest_queue"

    def __str__(self) -> str:
        return str(self.value)
