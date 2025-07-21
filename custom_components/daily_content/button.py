from homeassistant.components.button import ButtonEntity
from .const import DOMAIN

class PoetryRefreshButton(ButtonEntity):
    def __init__(self, coordinator):
        self.coordinator = coordinator
        self._attr_unique_id = f"{DOMAIN}_poetry_refresh"
        self._attr_name = "刷新每日诗词"
        self._attr_icon = "mdi:refresh"

    async def async_press(self):
        await self.coordinator.async_request_refresh()

class EnglishRefreshButton(ButtonEntity):
    def __init__(self, coordinator):
        self.coordinator = coordinator
        self._attr_unique_id = f"{DOMAIN}_english_refresh"
        self._attr_name = "刷新每日英语"
        self._attr_icon = "mdi:refresh"

    async def async_press(self):
        await self.coordinator.async_request_refresh()

async def async_setup_entry(hass, entry, async_add_entities):
    coordinators = hass.data[DOMAIN]
    async_add_entities([
        PoetryRefreshButton(coordinators["poetry_coordinator"]),
        EnglishRefreshButton(coordinators["english_coordinator"])
    ])