"""Constants for the argonone integration."""

from enum import Enum

DOMAIN = "Argon40"
CPU_TEMP_FILE = "/sys/class/thermal/thermal_zone0/temp"


class DeviceModel(Enum):
    """Device models."""

    ARGON_ONE_V2 = "ArgonOne V2"
