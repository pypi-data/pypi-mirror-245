from enum import Enum


class ProcessInformationMaterialFlowProcessType(str, Enum):
    CONVEYING = "Conveying"
    HANDLING = "Handling"
    STORAGE = "Storage"

    def __str__(self) -> str:
        return str(self.value)
