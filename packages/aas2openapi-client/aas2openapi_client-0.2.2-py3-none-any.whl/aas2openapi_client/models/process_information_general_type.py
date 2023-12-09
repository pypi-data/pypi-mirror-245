from enum import Enum


class ProcessInformationGeneralType(str, Enum):
    ASSEMBLY = "Assembly"
    MANUFACTURING = "Manufacturing"
    MATERIAL_FLOW = "Material Flow"
    REMANUFACTURING = "Remanufacturing"

    def __str__(self) -> str:
        return str(self.value)
