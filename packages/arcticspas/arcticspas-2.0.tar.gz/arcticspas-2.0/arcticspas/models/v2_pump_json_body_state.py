from enum import Enum


class V2PumpJsonBodyState(str, Enum):
    HIGH = "high"
    LOW = "low"
    OFF = "off"
    ON = "on"

    def __str__(self) -> str:
        return str(self.value)
