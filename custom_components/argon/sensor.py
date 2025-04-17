"""CPU Sensor."""

import asyncio
from decimal import Decimal, InvalidOperation
from pathlib import Path

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import CPU_TEMP_FILE


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up entry."""
    async_add_entities([CpuTemperatureSensor()])


class CpuTemperatureSensor(SensorEntity):
    """processor temperature sensor."""

    def __init__(self) -> None:
        """Initialize."""
        self._attr_name = "CPU Temperature"
        self.attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
        self._attr_unique_id = "cpu_temp_sensor"

    async def async_update(self) -> None:
        """Update sensor value."""

        def read_cpu_temp() -> Decimal | None:
            try:
                p = Path(CPU_TEMP_FILE)
                with p.open(mode="r", encoding="utf-8") as f:
                    return Decimal(f.read()) / 1000
            except (OSError, FileNotFoundError, InvalidOperation):
                return None

        self._attr_native_value = await asyncio.to_thread(read_cpu_temp)
