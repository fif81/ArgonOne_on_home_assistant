"""Config flow for ArgonOne integration."""

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.helpers.selector import (
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
)

from .const import DOMAIN, DeviceModel

_LOGGER = logging.getLogger(__name__)


class Argon40ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Argon."""

    VERSION = 1
    MINOR_VERSION = 0

    def __init__(self) -> None:
        """Initialize the config flow."""
        self.device_model = None

        self.options = {
            vol.Required("device_model"): SelectSelector(
                SelectSelectorConfig(
                    options=[e.value for e in DeviceModel],
                    sort=True,
                    mode=SelectSelectorMode.DROPDOWN,
                    translation_key="device_model_select",
                )
            ),
        }

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Handle the device step."""
        if user_input is not None:
            self.device_model = user_input.get("device_model")
            return self.async_create_entry(
                title=self.device_model,
                data={"device_model": self.device_model}
            )

        return self.async_show_form(
            step_id="user", data_schema=vol.Schema(self.options)
        )
