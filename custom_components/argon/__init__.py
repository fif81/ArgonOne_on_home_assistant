"""The argonone integration."""

from __future__ import annotations

import logging

from homeassistant.components.sensor import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv

from .const import DOMAIN
from .coordinator import Argon40Coordinator
from .hardware_controller import HardwareController

# _PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.FAN]
CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)
# CONFIG_SCHEMA = cv.empty_config_schema(DOMAIN)

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.FAN, Platform.SENSOR]

HARDWARE_CONTROLLER: HardwareController = HardwareController()


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Set up config entries."""

    coordinator = Argon40Coordinator(hass, config_entry, HARDWARE_CONTROLLER)
    config_entry.coordinator = coordinator

    config_entry.async_on_unload(
        config_entry.add_update_listener(_async_update_listener)
    )

    await hass.config_entries.async_forward_entry_setups(config_entry, PLATFORMS)
    await coordinator.async_config_entry_first_refresh()
    return True


async def _async_update_listener(
    hass: HomeAssistant, config_entry: ConfigEntry
) -> None:
    """Handle config options update."""
    await hass.config_entries.async_reload(config_entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Unload config entries."""
    await hass.config_entries.async_unload_platforms(config_entry, PLATFORMS)
    return True
