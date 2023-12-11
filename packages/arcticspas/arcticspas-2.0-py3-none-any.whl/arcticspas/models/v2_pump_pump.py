from enum import Enum


class V2PumpPump(str, Enum):
    ALL = "all"
    VALUE_0 = "1"
    VALUE_1 = "2"
    VALUE_2 = "3"
    VALUE_3 = "4"
    VALUE_4 = "5"

    def __str__(self) -> str:
        return str(self.value)
