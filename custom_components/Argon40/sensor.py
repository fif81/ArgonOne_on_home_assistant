"""CPU Sensor."""

import logging
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up entry."""
    coordinator = entry.coordinator
    async_add_entities([CpuTemperatureSensor(coordinator, entry.entry_id)])


class CpuTemperatureSensor(SensorEntity, CoordinatorEntity):
    """processor temperature sensor."""

    def __init__(self, coordinator: Any, entry_id: str) -> None:
        """Initialize."""
        super().__init__(coordinator)
        self._attr_name = "CPU Temperature"
        self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
        self._attr_device_class = SensorDeviceClass.TEMPERATURE
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self.unique_id = f"{entry_id}_cpu_temp"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        if "temperature" in self.coordinator.data:
            self._attr_native_value = self.coordinator.data["temperature"]
        super()._handle_coordinator_update()
