from enum import Enum


class ResourceInformationResourceType(str, Enum):
    MANUFACTURING = "Manufacturing"
    MATERIAL_FLOW = "Material Flow"
    STORAGE = "Storage"

    def __str__(self) -> str:
        return str(self.value)
