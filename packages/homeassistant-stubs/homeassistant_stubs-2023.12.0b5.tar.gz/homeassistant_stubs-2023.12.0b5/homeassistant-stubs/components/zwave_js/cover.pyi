from .const import COVER_POSITION_PROPERTY_KEYS as COVER_POSITION_PROPERTY_KEYS, COVER_TILT_PROPERTY_KEYS as COVER_TILT_PROPERTY_KEYS, DATA_CLIENT as DATA_CLIENT, DOMAIN as DOMAIN
from .discovery import ZwaveDiscoveryInfo as ZwaveDiscoveryInfo
from .discovery_data_template import CoverTiltDataTemplate as CoverTiltDataTemplate
from .entity import ZWaveBaseEntity as ZWaveBaseEntity
from _typeshed import Incomplete
from homeassistant.components.cover import ATTR_POSITION as ATTR_POSITION, ATTR_TILT_POSITION as ATTR_TILT_POSITION, CoverDeviceClass as CoverDeviceClass, CoverEntity as CoverEntity, CoverEntityFeature as CoverEntityFeature
from homeassistant.config_entries import ConfigEntry as ConfigEntry
from homeassistant.core import HomeAssistant as HomeAssistant, callback as callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect as async_dispatcher_connect
from homeassistant.helpers.entity_platform import AddEntitiesCallback as AddEntitiesCallback
from typing import Any
from zwave_js_server.model.driver import Driver as Driver
from zwave_js_server.model.value import Value as ZwaveValue

PARALLEL_UPDATES: int

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None: ...

class CoverPositionMixin(ZWaveBaseEntity, CoverEntity):
    _current_position_value: ZwaveValue | None
    _target_position_value: ZwaveValue | None
    _stop_position_value: ZwaveValue | None
    _attr_supported_features: Incomplete
    def _set_position_values(self, current_value: ZwaveValue, target_value: ZwaveValue | None = ..., stop_value: ZwaveValue | None = ...) -> None: ...
    def percent_to_zwave_position(self, value: int) -> int: ...
    def zwave_to_percent_position(self, value: int) -> int: ...
    @property
    def _fully_open_position(self) -> int: ...
    @property
    def _fully_closed_position(self) -> int: ...
    @property
    def _position_range(self) -> int: ...
    @property
    def is_closed(self) -> bool | None: ...
    @property
    def current_cover_position(self) -> int | None: ...
    async def async_set_cover_position(self, **kwargs: Any) -> None: ...
    async def async_open_cover(self, **kwargs: Any) -> None: ...
    async def async_close_cover(self, **kwargs: Any) -> None: ...
    async def async_stop_cover(self, **kwargs: Any) -> None: ...

class CoverTiltMixin(ZWaveBaseEntity, CoverEntity):
    _current_tilt_value: ZwaveValue | None
    _target_tilt_value: ZwaveValue | None
    _stop_tilt_value: ZwaveValue | None
    _attr_supported_features: Incomplete
    def _set_tilt_values(self, current_value: ZwaveValue, target_value: ZwaveValue | None = ..., stop_value: ZwaveValue | None = ...) -> None: ...
    def percent_to_zwave_tilt(self, value: int) -> int: ...
    def zwave_to_percent_tilt(self, value: int) -> int: ...
    @property
    def _fully_open_tilt(self) -> int: ...
    @property
    def _fully_closed_tilt(self) -> int: ...
    @property
    def _tilt_range(self) -> int: ...
    @property
    def current_cover_tilt_position(self) -> int | None: ...
    async def async_set_cover_tilt_position(self, **kwargs: Any) -> None: ...
    async def async_open_cover_tilt(self, **kwargs: Any) -> None: ...
    async def async_close_cover_tilt(self, **kwargs: Any) -> None: ...
    async def async_stop_cover_tilt(self, **kwargs: Any) -> None: ...

class ZWaveMultilevelSwitchCover(CoverPositionMixin):
    _attr_device_class: Incomplete
    def __init__(self, config_entry: ConfigEntry, driver: Driver, info: ZwaveDiscoveryInfo) -> None: ...

class ZWaveTiltCover(ZWaveMultilevelSwitchCover, CoverTiltMixin):
    def __init__(self, config_entry: ConfigEntry, driver: Driver, info: ZwaveDiscoveryInfo) -> None: ...

class ZWaveWindowCovering(CoverPositionMixin, CoverTiltMixin):
    _attr_name: Incomplete
    _attr_device_class: Incomplete
    def __init__(self, config_entry: ConfigEntry, driver: Driver, info: ZwaveDiscoveryInfo) -> None: ...
    @property
    def _fully_open_tilt(self) -> int: ...
    @property
    def _fully_closed_tilt(self) -> int: ...
    @property
    def _tilt_range(self) -> int: ...

class ZwaveMotorizedBarrier(ZWaveBaseEntity, CoverEntity):
    _attr_supported_features: Incomplete
    _attr_device_class: Incomplete
    _target_state: Incomplete
    def __init__(self, config_entry: ConfigEntry, driver: Driver, info: ZwaveDiscoveryInfo) -> None: ...
    @property
    def is_opening(self) -> bool | None: ...
    @property
    def is_closing(self) -> bool | None: ...
    @property
    def is_closed(self) -> bool | None: ...
    async def async_open_cover(self, **kwargs: Any) -> None: ...
    async def async_close_cover(self, **kwargs: Any) -> None: ...
