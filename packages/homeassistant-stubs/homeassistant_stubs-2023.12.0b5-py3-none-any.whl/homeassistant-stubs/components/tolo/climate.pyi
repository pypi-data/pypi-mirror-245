from . import ToloSaunaCoordinatorEntity as ToloSaunaCoordinatorEntity, ToloSaunaUpdateCoordinator as ToloSaunaUpdateCoordinator
from .const import DEFAULT_MAX_HUMIDITY as DEFAULT_MAX_HUMIDITY, DEFAULT_MAX_TEMP as DEFAULT_MAX_TEMP, DEFAULT_MIN_HUMIDITY as DEFAULT_MIN_HUMIDITY, DEFAULT_MIN_TEMP as DEFAULT_MIN_TEMP, DOMAIN as DOMAIN
from _typeshed import Incomplete
from homeassistant.components.climate import ClimateEntity as ClimateEntity, ClimateEntityFeature as ClimateEntityFeature, FAN_OFF as FAN_OFF, FAN_ON as FAN_ON, HVACAction as HVACAction, HVACMode as HVACMode
from homeassistant.config_entries import ConfigEntry as ConfigEntry
from homeassistant.const import ATTR_TEMPERATURE as ATTR_TEMPERATURE, PRECISION_WHOLE as PRECISION_WHOLE, UnitOfTemperature as UnitOfTemperature
from homeassistant.core import HomeAssistant as HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback as AddEntitiesCallback
from typing import Any

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None: ...

class SaunaClimate(ToloSaunaCoordinatorEntity, ClimateEntity):
    _attr_fan_modes: Incomplete
    _attr_hvac_modes: Incomplete
    _attr_max_humidity = DEFAULT_MAX_HUMIDITY
    _attr_max_temp = DEFAULT_MAX_TEMP
    _attr_min_humidity = DEFAULT_MIN_HUMIDITY
    _attr_min_temp = DEFAULT_MIN_TEMP
    _attr_name: Incomplete
    _attr_precision = PRECISION_WHOLE
    _attr_supported_features: Incomplete
    _attr_target_temperature_step: int
    _attr_temperature_unit: Incomplete
    _attr_unique_id: Incomplete
    def __init__(self, coordinator: ToloSaunaUpdateCoordinator, entry: ConfigEntry) -> None: ...
    @property
    def current_temperature(self) -> int: ...
    @property
    def current_humidity(self) -> int: ...
    @property
    def target_temperature(self) -> int: ...
    @property
    def target_humidity(self) -> int: ...
    @property
    def hvac_mode(self) -> HVACMode: ...
    @property
    def hvac_action(self) -> HVACAction | None: ...
    @property
    def fan_mode(self) -> str: ...
    def set_hvac_mode(self, hvac_mode: HVACMode) -> None: ...
    def set_fan_mode(self, fan_mode: str) -> None: ...
    def set_humidity(self, humidity: int) -> None: ...
    def set_temperature(self, **kwargs: Any) -> None: ...
    def _set_power_and_fan(self, power_on: bool, fan_on: bool) -> None: ...
