from enum import Enum


class SubProductStatus(str, Enum):
    ASSEMBLED = "assembled"
    UNASSEMBLED = "unassembled"

    def __str__(self) -> str:
        return str(self.value)
