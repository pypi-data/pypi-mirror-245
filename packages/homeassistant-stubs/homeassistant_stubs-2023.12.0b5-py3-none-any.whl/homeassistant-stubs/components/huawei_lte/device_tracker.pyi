from . import HuaweiLteBaseEntity as HuaweiLteBaseEntity, Router as Router
from .const import CONF_TRACK_WIRED_CLIENTS as CONF_TRACK_WIRED_CLIENTS, DEFAULT_TRACK_WIRED_CLIENTS as DEFAULT_TRACK_WIRED_CLIENTS, DOMAIN as DOMAIN, KEY_LAN_HOST_INFO as KEY_LAN_HOST_INFO, KEY_WLAN_HOST_LIST as KEY_WLAN_HOST_LIST, UPDATE_SIGNAL as UPDATE_SIGNAL
from _typeshed import Incomplete
from dataclasses import dataclass
from homeassistant.components.device_tracker import ScannerEntity as ScannerEntity, SourceType as SourceType
from homeassistant.config_entries import ConfigEntry as ConfigEntry
from homeassistant.core import HomeAssistant as HomeAssistant, callback as callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect as async_dispatcher_connect
from homeassistant.helpers.entity import Entity as Entity
from homeassistant.helpers.entity_platform import AddEntitiesCallback as AddEntitiesCallback
from typing import Any

_LOGGER: Incomplete
_DEVICE_SCAN: Incomplete
_HostType = dict[str, Any]

def _get_hosts(router: Router, ignore_subscriptions: bool = ...) -> list[_HostType] | None: ...
async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None: ...
def _is_wireless(host: _HostType) -> bool: ...
def _is_connected(host: _HostType | None) -> bool: ...
def _is_us(host: _HostType) -> bool: ...
def async_add_new_entities(router: Router, async_add_entities: AddEntitiesCallback, tracked: set[str]) -> None: ...
def _better_snakecase(text: str) -> str: ...

@dataclass
class HuaweiLteScannerEntity(HuaweiLteBaseEntity, ScannerEntity):
    _mac_address: str
    _ip_address: str | None = ...
    _is_connected: bool = ...
    _hostname: str | None = ...
    _extra_state_attributes: dict[str, Any] = ...
    @property
    def name(self) -> str: ...
    @property
    def _device_unique_id(self) -> str: ...
    @property
    def source_type(self) -> SourceType: ...
    @property
    def ip_address(self) -> str | None: ...
    @property
    def mac_address(self) -> str: ...
    @property
    def hostname(self) -> str | None: ...
    @property
    def is_connected(self) -> bool: ...
    @property
    def extra_state_attributes(self) -> dict[str, Any]: ...
    _available = ...
    async def async_update(self) -> None: ...
    def __init__(self, router, _mac_address) -> None: ...
