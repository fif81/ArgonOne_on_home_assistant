"""The argonone integration."""

from __future__ import annotations

import logging

from homeassistant.components.fan import DOMAIN as FAN_DOMAIN
from homeassistant.components.sensor import DOMAIN as SENSOR_DOMAIN, ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN

# _PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.FAN]
CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)
# CONFIG_SCHEMA = cv.empty_config_schema(DOMAIN)

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up ArgonOne."""
    return True


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Set up config entries."""

    await hass.config_entries.async_forward_entry_setups(
        config_entry, [FAN_DOMAIN, SENSOR_DOMAIN]
    )
    return True


async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Unload config entries."""
    await hass.config_entries.async_unload_platforms(
        config_entry, [FAN_DOMAIN, SENSOR_DOMAIN]
    )
    return True

