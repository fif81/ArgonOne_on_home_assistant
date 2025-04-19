"""CPU Sensor."""

import logging
from typing import Any, override

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
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
    async_add_entities([CpuTemperatureSensor(coordinator)], update_before_add=True)


class CpuTemperatureSensor(SensorEntity, CoordinatorEntity):
    """processor temperature sensor."""

    def __init__(self, coordinator: Any) -> None:
        """Initialize."""
        super().__init__(coordinator)
        self._attr_name = "CPU Temperature"
        self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
        self._attr_device_class = SensorDeviceClass.TEMPERATURE
        self._attr_state_class = SensorStateClass.MEASUREMENT

    @property
    @override
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        if self.coordinator.data is not None:
            return self.coordinator.data["temperature"]
        return None
