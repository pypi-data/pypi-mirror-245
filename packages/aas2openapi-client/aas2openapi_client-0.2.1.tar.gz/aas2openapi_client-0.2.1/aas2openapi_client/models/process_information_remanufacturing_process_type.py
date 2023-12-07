from enum import Enum


class ProcessInformationRemanufacturingProcessType(str, Enum):
    CLEANING = "Cleaning"
    DISASSEMBLY = "Disassembly"
    INSPECTION = "Inspection"
    REMEDIATION = "Remediation"

    def __str__(self) -> str:
        return str(self.value)
