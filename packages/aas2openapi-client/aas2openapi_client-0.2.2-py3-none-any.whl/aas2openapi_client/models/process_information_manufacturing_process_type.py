from enum import Enum


class ProcessInformationManufacturingProcessType(str, Enum):
    CHANGING_MATERIAL_PROPERTIES = "Changing Material Properties"
    COATING = "Coating"
    CUTTING = "Cutting"
    FORMING = "Forming"
    JOINING = "Joining"
    PRIMARY_SHAPING = "Primary Shaping"

    def __str__(self) -> str:
        return str(self.value)
