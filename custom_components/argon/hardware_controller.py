"""Hardware controller module for Argon40 devices.

This module provides the HardwareController class to manage
the communication to Argon40 hardware.
"""

class HardwareController:
    """Hardware controller for Argon40 hardware."""

    def __init__(self) -> None:
        """Initialize the hardware controller."""
        self._attr_fan_speed = 0

    @property
    def fan_speed(self) -> int:
        """Return the current fan speed."""
        return self._attr_fan_speed

    def set_fan_speed(self, speed: int) -> None:
        """Set the fan speed."""
        if 0 <= speed <= 100:
            self._attr_fan_speed = speed
            # Add code to set the fan speed on the hardware
        else:
            raise ValueError("Fan speed must be between 0 and 100.")
