from enum import Enum


class ProcessInformationAssemblyProcessType(str, Enum):
    ADJUSTING = "Adjusting"
    HANDLING = "Handling"
    JOINING = "Joining"
    SPECIAL_OPERATIONS = "Special Operations"
    TESTING = "Testing"

    def __str__(self) -> str:
        return str(self.value)
