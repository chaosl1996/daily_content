from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from datetime import timedelta

from .const import (
    DOMAIN, CONF_POETRY_INTERVAL, CONF_ENGLISH_INTERVAL,
    DEFAULT_POETRY_INTERVAL, DEFAULT_ENGLISH_INTERVAL
)
from .sensor import PoetryCoordinator, EnglishCoordinator

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    # 诗词协调器
    poetry_interval = timedelta(seconds=entry.data.get(
        CONF_POETRY_INTERVAL, DEFAULT_POETRY_INTERVAL.total_seconds()
    ))
    poetry_coordinator = PoetryCoordinator(
        hass, 
        poetry_interval, 
        name="daily_content_poetry"  # 添加name参数
    )
    await poetry_coordinator.async_config_entry_first_refresh()

    # 英语协调器
    english_interval = timedelta(seconds=entry.data.get(
        CONF_ENGLISH_INTERVAL, DEFAULT_ENGLISH_INTERVAL.total_seconds()
    ))
    english_coordinator = EnglishCoordinator(
        hass, 
        english_interval, 
        name="daily_content_english"  # 添加name参数
    )
    await english_coordinator.async_config_entry_first_refresh()

    # 存储协调器
    hass.data[DOMAIN] = {
        "poetry_coordinator": poetry_coordinator,
        "english_coordinator": english_coordinator
    }

    # 转发到传感器和按钮
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor", "button"])
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, ["sensor", "button"])
    if unload_ok:
        hass.data.pop(DOMAIN)
    return unload_ok