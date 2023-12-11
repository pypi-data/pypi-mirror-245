from enum import Enum


class V2BlowerBlower(str, Enum):
    ALL = "all"
    VALUE_0 = "1"
    VALUE_1 = "2"

    def __str__(self) -> str:
        return str(self.value)
