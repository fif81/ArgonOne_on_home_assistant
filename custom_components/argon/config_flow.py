"""Config flow for ArgonOne integration."""

import logging

import voluptuous as vol

from homeassistant import config_entries

from .const import DOMAIN, DeviceModel

_LOGGER = logging.getLogger(__name__)


class ArgonOneConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for ArgonOne."""

    VERSION = 1
    SM_BUS_OPTION = [0, 1]

    def __init__(self) -> None:
        """Initialize the config flow."""
        self.device_model = None

    async def async_step_user(self, user_input=None) -> config_entries.ConfigFlowResult:
        """Handle the device step."""
        if user_input is not None:
            self.device_model = user_input.get("device_model")
            return self.async_create_entry(
                title=self.device_model,
                data={"device_model": DeviceModel.__getitem__(self.device_model)},
            )

        options = {
            vol.Required(
                "device_model",
                default=DeviceModel.ARGON_ONE_V2,
            ): vol.In([e.name for e in DeviceModel]),
        }

        return self.async_show_form(step_id="user", data_schema=vol.Schema(options))
