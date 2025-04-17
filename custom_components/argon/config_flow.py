"""Config flow for ArgonOne integration."""

import logging

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.helpers.selector import (
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
)

from .const import DOMAIN, DeviceModel

_LOGGER = logging.getLogger(__name__)


class ArgonOneConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Argon."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize the config flow."""
        self.device_model = None

    async def async_step_user(self, user_input=None) -> config_entries.ConfigFlowResult:
        """Handle the device step."""
        errors = {}
        if user_input is not None:
            self.device_model = user_input.get("device_model")
            try:
                return self.async_create_entry(
                    title=self.device_model,
                    data={
                        "device_model": DeviceModel.__getitem__(self.device_model).name
                    },
                )
            except:
                errors["base"] = "something_went_wrong"

        options = {
            vol.Required("device_model"): SelectSelector(
                SelectSelectorConfig(
                    options=[e.name for e in DeviceModel],
                    sort=True,
                    mode=SelectSelectorMode.DROPDOWN,
                    translation_key="device_model_options",
                )
            ),
        }

        return self.async_show_form(
            step_id="user", data_schema=vol.Schema(options), errors=errors
        )
