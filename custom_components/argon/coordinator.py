"""Argon40 DataUpdateCoordinator."""

import asyncio
from datetime import timedelta
from decimal import Decimal, InvalidOperation
import logging
from pathlib import Path

from config.custom_components.argon.fan import CpuFanController
from config.custom_components.argon.sensor import CpuTemperatureSensor
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.device_registry import DeviceEntryType
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import CPU_TEMP_FILE, DOMAIN
from .hardware_controller import HardwareController

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities
) -> None:
    """Set up entry."""
    coordinator = config_entry.coordinator
    await coordinator.async_config_entry_first_refresh()

    async_add_entities(
        [CpuTemperatureSensor(coordinator), CpuFanController(coordinator)]
    )


class Coordinator(DataUpdateCoordinator):
    """The coordinator."""

    def __init__(
        self,
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        hardware_controller: HardwareController,
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            config_entry=config_entry,
            update_interval=timedelta(seconds=30),
            # Set always_update to `False` if the data returned from the
            # api can be compared via `__eq__` to avoid duplicate updates
            # being dispatched to listeners
            always_update=True,
        )
        self.model = config_entry.data.get("device_model")
        self.hass = hass
        self._device = None
        self._hardware_controller = hardware_controller

    def set_cpu_fan_percentage(self, percentage: int) -> None:
        """Set the CPU fan percentage."""
        _LOGGER.debug("Setting fan percentage to %d%%", percentage)
        self._hardware_controller.set_fan_speed(percentage)

    async def _async_update_data(self):
        def read_cpu_temp() -> Decimal | None:
            try:
                p = Path(CPU_TEMP_FILE)
                with p.open(mode="r", encoding="utf-8") as f:
                    return Decimal(f.read()) / 1000
            except (OSError, FileNotFoundError, InvalidOperation) as exception:
                _LOGGER.error("Error reading CPU temperature: %s", exception)
                return None

        # try:
        # Note: asyncio.TimeoutError and aiohttp.ClientError are already
        # handled by the data update coordinator.

        async with asyncio.timeout(10):
            # Grab active context variables to limit data required to be fetched from API
            # Note: using context is not required if there is no need or ability to limit
            # data retrieved from API.
            result = {}
            result["temperature"] = await self.hass.async_add_executor_job(
                read_cpu_temp
            )
            # result["percentage"] = self._hardware_controller.fan_speed

        return result
        # except exception as err:
        # raise UpdateFailed(f"Error communicating with API: {err}") from err
