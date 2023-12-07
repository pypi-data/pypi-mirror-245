import logging
from .api import get_api_scopes as get_api_scopes
from .const import CONF_AREA_NAME as CONF_AREA_NAME, CONF_LAT_NE as CONF_LAT_NE, CONF_LAT_SW as CONF_LAT_SW, CONF_LON_NE as CONF_LON_NE, CONF_LON_SW as CONF_LON_SW, CONF_NEW_AREA as CONF_NEW_AREA, CONF_PUBLIC_MODE as CONF_PUBLIC_MODE, CONF_WEATHER_AREAS as CONF_WEATHER_AREAS, DOMAIN as DOMAIN
from _typeshed import Incomplete
from collections.abc import Mapping
from homeassistant import config_entries as config_entries
from homeassistant.const import CONF_SHOW_ON_MAP as CONF_SHOW_ON_MAP, CONF_UUID as CONF_UUID
from homeassistant.core import callback as callback
from homeassistant.data_entry_flow import FlowResult as FlowResult
from homeassistant.helpers import config_entry_oauth2_flow as config_entry_oauth2_flow
from typing import Any

_LOGGER: Incomplete

class NetatmoFlowHandler(config_entry_oauth2_flow.AbstractOAuth2FlowHandler, domain=DOMAIN):
    DOMAIN = DOMAIN
    @staticmethod
    def async_get_options_flow(config_entry: config_entries.ConfigEntry) -> config_entries.OptionsFlow: ...
    @property
    def logger(self) -> logging.Logger: ...
    @property
    def extra_authorize_data(self) -> dict: ...
    async def async_step_user(self, user_input: dict | None = ...) -> FlowResult: ...
    async def async_step_reauth(self, entry_data: Mapping[str, Any]) -> FlowResult: ...
    async def async_step_reauth_confirm(self, user_input: dict | None = ...) -> FlowResult: ...
    async def async_oauth_create_entry(self, data: dict) -> FlowResult: ...

class NetatmoOptionsFlowHandler(config_entries.OptionsFlow):
    config_entry: Incomplete
    options: Incomplete
    def __init__(self, config_entry: config_entries.ConfigEntry) -> None: ...
    async def async_step_init(self, user_input: dict | None = ...) -> FlowResult: ...
    async def async_step_public_weather_areas(self, user_input: dict | None = ...) -> FlowResult: ...
    async def async_step_public_weather(self, user_input: dict) -> FlowResult: ...
    def _create_options_entry(self) -> FlowResult: ...

def fix_coordinates(user_input: dict) -> dict: ...
