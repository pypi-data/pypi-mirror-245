import aiohttp
from .frame import warn_use as warn_use
from .json import json_dumps as json_dumps
from _typeshed import Incomplete
from aiohttp import web
from aiohttp.typedefs import JSONDecoder as JSONDecoder
from collections.abc import Awaitable, Callable as Callable
from homeassistant import config_entries as config_entries
from homeassistant.const import APPLICATION_NAME as APPLICATION_NAME, EVENT_HOMEASSISTANT_CLOSE as EVENT_HOMEASSISTANT_CLOSE, __version__ as __version__
from homeassistant.core import Event as Event, HomeAssistant as HomeAssistant, callback as callback
from homeassistant.loader import bind_hass as bind_hass
from homeassistant.util.json import json_loads as json_loads
from typing import Any

DATA_CONNECTOR: str
DATA_CLIENTSESSION: str
SERVER_SOFTWARE: Incomplete
ENABLE_CLEANUP_CLOSED: Incomplete
WARN_CLOSE_MSG: str
MAXIMUM_CONNECTIONS: int
MAXIMUM_CONNECTIONS_PER_HOST: int

class HassClientResponse(aiohttp.ClientResponse):
    async def json(self, *args: Any, loads: JSONDecoder = ..., **kwargs: Any) -> Any: ...

def async_get_clientsession(hass: HomeAssistant, verify_ssl: bool = ..., family: int = ...) -> aiohttp.ClientSession: ...
def async_create_clientsession(hass: HomeAssistant, verify_ssl: bool = ..., auto_cleanup: bool = ..., family: int = ..., **kwargs: Any) -> aiohttp.ClientSession: ...
def _async_create_clientsession(hass: HomeAssistant, verify_ssl: bool = ..., auto_cleanup_method: Callable[[HomeAssistant, aiohttp.ClientSession], None] | None = ..., family: int = ..., **kwargs: Any) -> aiohttp.ClientSession: ...
async def async_aiohttp_proxy_web(hass: HomeAssistant, request: web.BaseRequest, web_coro: Awaitable[aiohttp.ClientResponse], buffer_size: int = ..., timeout: int = ...) -> web.StreamResponse | None: ...
async def async_aiohttp_proxy_stream(hass: HomeAssistant, request: web.BaseRequest, stream: aiohttp.StreamReader, content_type: str | None, buffer_size: int = ..., timeout: int = ...) -> web.StreamResponse: ...
def _async_register_clientsession_shutdown(hass: HomeAssistant, clientsession: aiohttp.ClientSession) -> None: ...
def _async_register_default_clientsession_shutdown(hass: HomeAssistant, clientsession: aiohttp.ClientSession) -> None: ...
def _make_key(verify_ssl: bool = ..., family: int = ...) -> tuple[bool, int]: ...
def _async_get_connector(hass: HomeAssistant, verify_ssl: bool = ..., family: int = ...) -> aiohttp.BaseConnector: ...
