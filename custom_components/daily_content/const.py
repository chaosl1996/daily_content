from datetime import timedelta
import voluptuous as vol

DOMAIN = "daily_content"
CONF_POETRY_INTERVAL = "poetry_update_interval"
CONF_ENGLISH_INTERVAL = "english_update_interval"
DEFAULT_POETRY_INTERVAL = timedelta(hours=24)
DEFAULT_ENGLISH_INTERVAL = timedelta(hours=24)
POETRY_API_URL = "https://api.codelife.cc/todayShici?lang=cn"
ENGLISH_API_URL = "https://apis.tianapi.com/ensentence/index?key=5bc7cd35ce0ad775e11732a407a6885b"

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Optional(CONF_POETRY_INTERVAL, default=DEFAULT_POETRY_INTERVAL):
            vol.All(vol.Coerce(timedelta), vol.Range(min=timedelta(hours=1))),
        vol.Optional(CONF_ENGLISH_INTERVAL, default=DEFAULT_ENGLISH_INTERVAL):
            vol.All(vol.Coerce(timedelta), vol.Range(min=timedelta(hours=1))),
    })
}, extra=vol.ALLOW_EXTRA)