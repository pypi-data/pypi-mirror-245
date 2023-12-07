import aiounifi
from .const import ATTR_MANUFACTURER as ATTR_MANUFACTURER
from .controller import UNIFI_DOMAIN as UNIFI_DOMAIN, UniFiController as UniFiController
from .entity import HandlerT as HandlerT, SubscriptionT as SubscriptionT, UnifiEntity as UnifiEntity, UnifiEntityDescription as UnifiEntityDescription, async_client_device_info_fn as async_client_device_info_fn, async_device_available_fn as async_device_available_fn, async_device_device_info_fn as async_device_device_info_fn, async_wlan_device_info_fn as async_wlan_device_info_fn
from _typeshed import Incomplete
from aiounifi.interfaces.api_handlers import ItemEvent
from aiounifi.models.api import ApiItemT
from aiounifi.models.dpi_restriction_group import DPIRestrictionGroup
from aiounifi.models.event import Event as Event
from collections.abc import Callable as Callable, Coroutine
from dataclasses import dataclass
from homeassistant.components.switch import DOMAIN as DOMAIN, SwitchDeviceClass as SwitchDeviceClass, SwitchEntity as SwitchEntity, SwitchEntityDescription as SwitchEntityDescription
from homeassistant.config_entries import ConfigEntry as ConfigEntry
from homeassistant.const import EntityCategory as EntityCategory
from homeassistant.core import HomeAssistant as HomeAssistant, callback as callback
from homeassistant.helpers.device_registry import DeviceEntryType as DeviceEntryType, DeviceInfo as DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback as AddEntitiesCallback
from typing import Any, Generic

CLIENT_BLOCKED: Incomplete
CLIENT_UNBLOCKED: Incomplete

def async_block_client_allowed_fn(controller: UniFiController, obj_id: str) -> bool: ...
def async_dpi_group_is_on_fn(controller: UniFiController, dpi_group: DPIRestrictionGroup) -> bool: ...
def async_dpi_group_device_info_fn(controller: UniFiController, obj_id: str) -> DeviceInfo: ...
def async_port_forward_device_info_fn(controller: UniFiController, obj_id: str) -> DeviceInfo: ...
async def async_block_client_control_fn(controller: UniFiController, obj_id: str, target: bool) -> None: ...
async def async_dpi_group_control_fn(controller: UniFiController, obj_id: str, target: bool) -> None: ...
def async_outlet_supports_switching_fn(controller: UniFiController, obj_id: str) -> bool: ...
async def async_outlet_control_fn(controller: UniFiController, obj_id: str, target: bool) -> None: ...
async def async_poe_port_control_fn(controller: UniFiController, obj_id: str, target: bool) -> None: ...
async def async_port_forward_control_fn(controller: UniFiController, obj_id: str, target: bool) -> None: ...
async def async_wlan_control_fn(controller: UniFiController, obj_id: str, target: bool) -> None: ...

@dataclass
class UnifiSwitchEntityDescriptionMixin(Generic[HandlerT, ApiItemT]):
    control_fn: Callable[[UniFiController, str, bool], Coroutine[Any, Any, None]]
    is_on_fn: Callable[[UniFiController, ApiItemT], bool]
    def __init__(self, control_fn, is_on_fn) -> None: ...

@dataclass
class UnifiSwitchEntityDescription(SwitchEntityDescription, UnifiEntityDescription[HandlerT, ApiItemT], UnifiSwitchEntityDescriptionMixin[HandlerT, ApiItemT]):
    custom_subscribe: Callable[[aiounifi.Controller], SubscriptionT] | None = ...
    only_event_for_state_change: bool = ...
    def __init__(self, control_fn, is_on_fn, allowed_fn, api_handler_fn, available_fn, device_info_fn, event_is_on, event_to_subscribe, name_fn, object_fn, should_poll, supported_fn, unique_id_fn, key, device_class, entity_category, entity_registry_enabled_default, entity_registry_visible_default, force_update, icon, has_entity_name, name, translation_key, unit_of_measurement, custom_subscribe, only_event_for_state_change) -> None: ...

ENTITY_DESCRIPTIONS: tuple[UnifiSwitchEntityDescription, ...]

def async_update_unique_id(hass: HomeAssistant, config_entry: ConfigEntry) -> None: ...
async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None: ...

class UnifiSwitchEntity(UnifiEntity[HandlerT, ApiItemT], SwitchEntity):
    entity_description: UnifiSwitchEntityDescription[HandlerT, ApiItemT]
    only_event_for_state_change: bool
    def async_initiate_state(self) -> None: ...
    async def async_turn_on(self, **kwargs: Any) -> None: ...
    async def async_turn_off(self, **kwargs: Any) -> None: ...
    _attr_is_on: Incomplete
    def async_update_state(self, event: ItemEvent, obj_id: str) -> None: ...
    _attr_available: Incomplete
    def async_event_callback(self, event: Event) -> None: ...
    async def async_added_to_hass(self) -> None: ...
