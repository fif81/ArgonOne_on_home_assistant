"""CPU Fan."""

from typing import Any

from homeassistant.components.fan import FanEntity, FanEntityFeature
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up entry."""
    async_add_entities([CpuFanController()])


class CpuFanController(FanEntity):
    """CPU Fan Controller."""

    def __init__(self) -> None:
        """Initialize."""
        self._attr_name = "CPU Fan"
        self._attr_unique_id = "cpu_fan"
        self._attr_supported_features = (
            FanEntityFeature.SET_SPEED
            | FanEntityFeature.TURN_ON
            | FanEntityFeature.TURN_OFF
        )
        self._is_on = False
        self._speed = 0

    @property
    def is_on(self) -> bool | None:
        """Return if switched on."""
        return self._is_on

    @property
    def percentage(self) -> int:
        """Percentage of max speed."""
        return self._speed

    async def async_turn_on(
        self,
        percentage: int | None = None,
        preset_mode: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Turn fan on."""
        if percentage is None:
            await self.async_set_percentage(100)
        else:
            await self.async_set_percentage(percentage)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn fan off."""
        await self.async_set_percentage(0)

    async def async_set_percentage(self, percentage: int) -> None:
        """Set fan speed."""
        self._speed = percentage
        self._is_on = percentage > 0
