from . import async_discover_devices as async_discover_devices
from .const import DOMAIN as DOMAIN
from _typeshed import Incomplete
from homeassistant import config_entries as config_entries
from homeassistant.components import dhcp as dhcp
from homeassistant.const import CONF_DEVICE as CONF_DEVICE, CONF_HOST as CONF_HOST, CONF_MAC as CONF_MAC
from homeassistant.core import callback as callback
from homeassistant.data_entry_flow import FlowResult as FlowResult
from homeassistant.helpers.typing import DiscoveryInfoType as DiscoveryInfoType
from kasa import SmartDevice as SmartDevice
from typing import Any

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION: int
    _discovered_devices: Incomplete
    _discovered_device: Incomplete
    def __init__(self) -> None: ...
    async def async_step_dhcp(self, discovery_info: dhcp.DhcpServiceInfo) -> FlowResult: ...
    async def async_step_integration_discovery(self, discovery_info: DiscoveryInfoType) -> FlowResult: ...
    async def _async_handle_discovery(self, host: str, mac: str) -> FlowResult: ...
    async def async_step_discovery_confirm(self, user_input: dict[str, Any] | None = ...) -> FlowResult: ...
    async def async_step_user(self, user_input: dict[str, Any] | None = ...) -> FlowResult: ...
    async def async_step_pick_device(self, user_input: dict[str, Any] | None = ...) -> FlowResult: ...
    def _async_create_entry_from_device(self, device: SmartDevice) -> FlowResult: ...
    async def _async_try_connect(self, host: str, raise_on_progress: bool = ...) -> SmartDevice: ...
