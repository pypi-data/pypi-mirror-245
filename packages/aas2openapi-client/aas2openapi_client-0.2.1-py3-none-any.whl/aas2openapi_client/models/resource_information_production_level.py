from enum import Enum


class ResourceInformationProductionLevel(str, Enum):
    MODULE = "Module"
    NETWORK = "Network"
    PLANT = "Plant"
    STATION = "Station"
    SYSTEM = "System"

    def __str__(self) -> str:
        return str(self.value)
