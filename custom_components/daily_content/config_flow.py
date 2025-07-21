import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult

from .const import (
    DOMAIN, CONF_POETRY_INTERVAL, CONF_ENGLISH_INTERVAL,
    DEFAULT_POETRY_INTERVAL, DEFAULT_ENGLISH_INTERVAL
)

class DailyContentConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    async def async_step_user(self, user_input=None) -> FlowResult:
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema({
                    vol.Optional(
                        CONF_POETRY_INTERVAL,
                        default=DEFAULT_POETRY_INTERVAL.total_seconds() // 3600,
                    ): vol.All(vol.Coerce(int), vol.Range(min=1)),
                    vol.Optional(
                        CONF_ENGLISH_INTERVAL,
                        default=DEFAULT_ENGLISH_INTERVAL.total_seconds() // 3600,
                    ): vol.All(vol.Coerce(int), vol.Range(min=1)),
                })
            )

        # 转换小时为秒
        user_input[CONF_POETRY_INTERVAL] *= 3600
        user_input[CONF_ENGLISH_INTERVAL] *= 3600

        return self.async_create_entry(title="每日内容", data=user_input)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return OptionsFlowHandler(config_entry)

class OptionsFlowHandler(config_entries.OptionsFlow):
    async def async_step_init(self, user_input=None) -> FlowResult:
        if user_input:
            user_input[CONF_POETRY_INTERVAL] *= 3600
            user_input[CONF_ENGLISH_INTERVAL] *= 3600
            self.hass.config_entries.async_update_entry(self.config_entry, data=user_input)
            return self.async_create_entry(title="英语诗词", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Optional(
                    CONF_POETRY_INTERVAL,
                    default=self.config_entry.data[CONF_POETRY_INTERVAL] // 3600,
                ): vol.All(vol.Coerce(int), vol.Range(min=1)),
                vol.Optional(
                    CONF_ENGLISH_INTERVAL,
                    default=self.config_entry.data[CONF_ENGLISH_INTERVAL] // 3600,
                ): vol.All(vol.Coerce(int), vol.Range(min=1)),
            })
        )