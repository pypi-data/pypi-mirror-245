from .const import COORDINATOR as COORDINATOR, DEFAULT_SCAN_INTERVAL as DEFAULT_SCAN_INTERVAL, DOMAIN as DOMAIN, INTEGRATION_SUPPORTED_COMMANDS as INTEGRATION_SUPPORTED_COMMANDS, PLATFORMS as PLATFORMS, PYNUT_DATA as PYNUT_DATA, PYNUT_UNIQUE_ID as PYNUT_UNIQUE_ID, USER_AVAILABLE_COMMANDS as USER_AVAILABLE_COMMANDS
from _typeshed import Incomplete
from dataclasses import dataclass
from homeassistant.config_entries import ConfigEntry as ConfigEntry
from homeassistant.const import CONF_ALIAS as CONF_ALIAS, CONF_HOST as CONF_HOST, CONF_PASSWORD as CONF_PASSWORD, CONF_PORT as CONF_PORT, CONF_RESOURCES as CONF_RESOURCES, CONF_SCAN_INTERVAL as CONF_SCAN_INTERVAL, CONF_USERNAME as CONF_USERNAME
from homeassistant.core import HomeAssistant as HomeAssistant
from homeassistant.exceptions import HomeAssistantError as HomeAssistantError
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator as DataUpdateCoordinator, UpdateFailed as UpdateFailed

NUT_FAKE_SERIAL: Incomplete
_LOGGER: Incomplete

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool: ...
async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool: ...
async def _async_update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None: ...
def _manufacturer_from_status(status: dict[str, str]) -> str | None: ...
def _model_from_status(status: dict[str, str]) -> str | None: ...
def _firmware_from_status(status: dict[str, str]) -> str | None: ...
def _serial_from_status(status: dict[str, str]) -> str | None: ...
def _unique_id_from_status(status: dict[str, str]) -> str | None: ...

@dataclass
class NUTDeviceInfo:
    manufacturer: str | None = ...
    model: str | None = ...
    firmware: str | None = ...
    def __init__(self, manufacturer, model, firmware) -> None: ...

class PyNUTData:
    _host: Incomplete
    _alias: Incomplete
    _client: Incomplete
    ups_list: Incomplete
    _status: Incomplete
    _device_info: Incomplete
    def __init__(self, host: str, port: int, alias: str | None, username: str | None, password: str | None) -> None: ...
    @property
    def status(self) -> dict[str, str] | None: ...
    @property
    def name(self) -> str: ...
    @property
    def device_info(self) -> NUTDeviceInfo: ...
    def _get_alias(self) -> str | None: ...
    def _get_device_info(self) -> NUTDeviceInfo | None: ...
    def _get_status(self) -> dict[str, str] | None: ...
    def update(self) -> None: ...
    async def async_run_command(self, hass: HomeAssistant, command_name: str | None) -> None: ...
    def list_commands(self) -> dict[str, str] | None: ...
