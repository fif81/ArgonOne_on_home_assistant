"""Config flow for ArgonOne integration."""

import logging

from config_entries import ConfigFlowResult
import voluptuous as vol

from homeassistant import config_entries

_LOGGER = logging.getLogger(__name__)


class ArgonOneConfigFlow(config_entries.ConfigFlow, domain="argonone"):
    """Handle a config flow for ArgonOne."""

    VERSION = 1
    SM_BUS_OPTION = [0, 1]

    def __init__(self) -> None:
        """Initialize the config flow."""
        self.smbus = None

    async def async_step_user(self, user_input=None) -> ConfigFlowResult:
        """Handle the user step."""
        if user_input is not None:
            self.smbus = user_input.get("smbus")
            return self.async_create_entry(
                title="ArgonOne Fan Controller", data={"smbus": self.smbus}
            )

        options = {
            vol.Required("smbus", default=0): vol.In(self.SM_BUS_OPTION),
        }

        return self.async_show_form(step_id="user", data_schema=vol.Schema(options))

