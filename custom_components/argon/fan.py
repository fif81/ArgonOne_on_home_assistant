"""CPU Fan."""

import logging
from typing import Any, override

from homeassistant.components.fan import FanEntity, FanEntityFeature
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up entry."""
    coordinator = entry.coordinator
    async_add_entities([CpuFanController(coordinator, entry.entry_id)])


class CpuFanController(FanEntity, CoordinatorEntity):
    """CPU Fan Controller."""

    def __init__(self, coordinator: Any, entry_id: str) -> None:
        """Initialize."""
        super().__init__(coordinator)
        self._attr_name = "CPU Fan"
        self._attr_supported_features = (
            FanEntityFeature.SET_SPEED
            | FanEntityFeature.TURN_OFF
            | FanEntityFeature.TURN_ON
        )
        self._attr_is_on = False
        self._attr_percentage = 0
        self.unique_id = f"{entry_id}_fan"

        self._attr_device_info = {
            "identifiers": {(DOMAIN, f"{entry_id}_device")},
            "name": "CPU Fan",
            "manufacturer": "Argon40",
            "model": coordinator.model,
            "configuration_url": f"homeassistant://config/integrations/integration/{DOMAIN}",
            "connections": None,
            "entry_type": dr.DeviceEntryType.SERVICE,
            "hw_version": None,
            "sw_version": None,
            "suggested_area": None,
            "via_device": None,
        }

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        if "fan_speed" in self.coordinator.data:
            self.set_percentage(self.coordinator.data["fan_speed"])
        super()._handle_coordinator_update()

    @override
    async def async_set_percentage(self, percentage: int) -> None:
        """Set the speed of the fan, as a percentage."""
        await super().async_set_percentage(percentage)
        await self.coordinator.async_refresh()

    @override
    def set_percentage(self, percentage: int) -> None:
        """Set the speed of the fan, as a percentage."""
        self.coordinator.set_cpu_fan_percentage(percentage)
        self._attr_percentage = percentage
        self._attr_is_on = percentage > 0

    @override
    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the entity off."""
        await super().async_turn_off(**kwargs)
        await self.coordinator.async_refresh()

    @override
    def turn_off(self, **kwargs: Any) -> None:
        """Turn the entity off."""
        self.set_percentage(0)

    async def async_turn_on(
        self,
        percentage: int | None = None,
        preset_mode: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Turn the entity on."""
        await super().async_turn_on(**kwargs)
        await self.coordinator.async_refresh()

    def turn_on(
        self,
        percentage: int | None = None,
        preset_mode: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Turn the entity on."""
        if percentage is not None:
            self.set_percentage(percentage)
        else:
            self.set_percentage(100)
