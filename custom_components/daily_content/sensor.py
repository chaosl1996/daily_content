import aiohttp
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
import logging

from .const import DOMAIN, POETRY_API_URL, ENGLISH_API_URL

# 诗词协调器和传感器
class PoetryCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, update_interval, name):
        super().__init__(
            hass,
            logger=logging.getLogger(__name__),
            name=name,
            update_interval=update_interval
        )

    async def _async_update_data(self):
        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
                    'Origin': 'https://go.itab.link',
                    'Signaturekey': 'U2FsdGVkX1/+tbsZ0ZVVItoYYzjoeoNeWMOBXuelSkA='
                }
                async with session.get(POETRY_API_URL, headers=headers) as response:
                    if response.status != 200:
                        raise UpdateFailed(f"诗词API错误: {response.status}")
                    data = await response.json()
                    if data.get("code") != 200:
                        raise UpdateFailed(f"诗词API错误: {data.get('msg')}")
                    return data["data"]
        except Exception as e:
            raise UpdateFailed(f"获取诗词失败: {str(e)}")

class PoetrySensor(SensorEntity):
    def __init__(self, coordinator):
        self.coordinator = coordinator
        self._attr_unique_id = f"{DOMAIN}_poetry"
        self._attr_name = "每日诗词"
        self.coordinator.async_add_listener(self.async_write_ha_state)

    @property
    def state(self):
        return self.coordinator.data.get("quotes") if self.coordinator.data else None

    @property
    def extra_state_attributes(self):
        if not self.coordinator.data: return {}
        data = self.coordinator.data
        return {
            "author": data.get("author"),
            "dynasty": data.get("dynasty"),
            "title": data.get("title"),
            "content": data.get("content")
        }

# 英语协调器和传感器
class EnglishCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, update_interval, name):
        super().__init__(
            hass,
            logger=logging.getLogger(__name__),
            name=name,
            update_interval=update_interval
        )

    async def _async_update_data(self):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(ENGLISH_API_URL) as response:
                    if response.status != 200:
                        raise UpdateFailed(f"英语API错误: {response.status}")
                    data = await response.json()
                    if data.get("code") != 200:
                        raise UpdateFailed(f"英语API错误: {data.get('msg')}")
                    return data["result"]
        except Exception as e:
            raise UpdateFailed(f"获取英语失败: {str(e)}")

class EnglishSensor(SensorEntity):
    def __init__(self, coordinator):
        self.coordinator = coordinator
        self._attr_unique_id = f"{DOMAIN}_english"
        self._attr_name = "每日英语"
        self.coordinator.async_add_listener(self.async_write_ha_state)

    @property
    def state(self):
        return self.coordinator.data.get("en") if self.coordinator.data else None

    @property
    def extra_state_attributes(self):
        if not self.coordinator.data: return {}
        return {"translation": self.coordinator.data.get("zh")}

# 传感器设置
async def async_setup_entry(hass, entry, async_add_entities):
    coordinators = hass.data[DOMAIN]
    async_add_entities([
        PoetrySensor(coordinators["poetry_coordinator"]),
        EnglishSensor(coordinators["english_coordinator"])
    ])