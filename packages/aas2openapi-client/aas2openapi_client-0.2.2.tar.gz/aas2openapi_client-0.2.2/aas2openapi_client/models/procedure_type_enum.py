from enum import Enum


class ProcedureTypeEnum(str, Enum):
    BREAKDOWN = "Breakdown"
    LOADING = "Loading"
    MAINTENANCE = "Maintenance"
    NONSCHEDULED = "NonScheduled"
    PRODUCTION = "Production"
    REPAIR = "Repair"
    SETUP = "Setup"
    TRANSPORT = "Transport"

    def __str__(self) -> str:
        return str(self.value)
