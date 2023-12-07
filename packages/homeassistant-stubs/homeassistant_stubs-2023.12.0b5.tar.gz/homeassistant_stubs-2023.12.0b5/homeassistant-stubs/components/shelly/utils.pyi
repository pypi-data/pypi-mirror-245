from .const import BASIC_INPUTS_EVENTS_TYPES as BASIC_INPUTS_EVENTS_TYPES, CONF_COAP_PORT as CONF_COAP_PORT, DEFAULT_COAP_PORT as DEFAULT_COAP_PORT, DEVICES_WITHOUT_FIRMWARE_CHANGELOG as DEVICES_WITHOUT_FIRMWARE_CHANGELOG, DOMAIN as DOMAIN, GEN1_RELEASE_URL as GEN1_RELEASE_URL, GEN2_RELEASE_URL as GEN2_RELEASE_URL, LOGGER as LOGGER, RPC_INPUTS_EVENTS_TYPES as RPC_INPUTS_EVENTS_TYPES, SHBTN_INPUTS_EVENTS_TYPES as SHBTN_INPUTS_EVENTS_TYPES, SHBTN_MODELS as SHBTN_MODELS, SHIX3_1_INPUTS_EVENTS_TYPES as SHIX3_1_INPUTS_EVENTS_TYPES, UPTIME_DEVIATION as UPTIME_DEVIATION
from _typeshed import Incomplete
from aiohttp.web import Request as Request, WebSocketResponse as WebSocketResponse
from aioshelly.block_device import Block as Block, BlockDevice as BlockDevice, COAP
from aioshelly.rpc_device import RpcDevice as RpcDevice, WsServer
from datetime import datetime
from homeassistant.components.http import HomeAssistantView as HomeAssistantView
from homeassistant.config_entries import ConfigEntry as ConfigEntry
from homeassistant.const import EVENT_HOMEASSISTANT_STOP as EVENT_HOMEASSISTANT_STOP
from homeassistant.core import Event as Event, HomeAssistant as HomeAssistant, callback as callback
from homeassistant.helpers import singleton as singleton
from homeassistant.helpers.device_registry import CONNECTION_NETWORK_MAC as CONNECTION_NETWORK_MAC, format_mac as format_mac
from homeassistant.util.dt import utcnow as utcnow
from typing import Any

def async_remove_shelly_entity(hass: HomeAssistant, domain: str, unique_id: str) -> None: ...
def get_number_of_channels(device: BlockDevice, block: Block) -> int: ...
def get_block_entity_name(device: BlockDevice, block: Block | None, description: str | None = ...) -> str: ...
def get_block_channel_name(device: BlockDevice, block: Block | None) -> str: ...
def is_block_momentary_input(settings: dict[str, Any], block: Block, include_detached: bool = ...) -> bool: ...
def get_device_uptime(uptime: float, last_uptime: datetime | None) -> datetime: ...
def get_block_input_triggers(device: BlockDevice, block: Block) -> list[tuple[str, str]]: ...
def get_shbtn_input_triggers() -> list[tuple[str, str]]: ...
async def get_coap_context(hass: HomeAssistant) -> COAP: ...

class ShellyReceiver(HomeAssistantView):
    requires_auth: bool
    url: str
    name: str
    _ws_server: Incomplete
    def __init__(self, ws_server: WsServer) -> None: ...
    async def get(self, request: Request) -> WebSocketResponse: ...

async def get_ws_context(hass: HomeAssistant) -> WsServer: ...
def get_block_device_sleep_period(settings: dict[str, Any]) -> int: ...
def get_rpc_device_sleep_period(config: dict[str, Any]) -> int: ...
def get_rpc_device_wakeup_period(status: dict[str, Any]) -> int: ...
def get_info_auth(info: dict[str, Any]) -> bool: ...
def get_info_gen(info: dict[str, Any]) -> int: ...
def get_model_name(info: dict[str, Any]) -> str: ...
def get_rpc_channel_name(device: RpcDevice, key: str) -> str: ...
def get_rpc_entity_name(device: RpcDevice, key: str, description: str | None = ...) -> str: ...
def get_device_entry_gen(entry: ConfigEntry) -> int: ...
def get_rpc_key_instances(keys_dict: dict[str, Any], key: str) -> list[str]: ...
def get_rpc_key_ids(keys_dict: dict[str, Any], key: str) -> list[int]: ...
def is_rpc_momentary_input(config: dict[str, Any], status: dict[str, Any], key: str) -> bool: ...
def is_block_channel_type_light(settings: dict[str, Any], channel: int) -> bool: ...
def is_rpc_channel_type_light(config: dict[str, Any], channel: int) -> bool: ...
def get_rpc_input_triggers(device: RpcDevice) -> list[tuple[str, str]]: ...
def update_device_fw_info(hass: HomeAssistant, shellydevice: BlockDevice | RpcDevice, entry: ConfigEntry) -> None: ...
def brightness_to_percentage(brightness: int) -> int: ...
def percentage_to_brightness(percentage: int) -> int: ...
def mac_address_from_name(name: str) -> str | None: ...
def get_release_url(gen: int, model: str, beta: bool) -> str | None: ...
