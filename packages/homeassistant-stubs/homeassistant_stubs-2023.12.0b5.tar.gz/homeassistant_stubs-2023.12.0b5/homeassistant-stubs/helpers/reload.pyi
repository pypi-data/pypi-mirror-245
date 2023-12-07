from . import config_per_platform as config_per_platform
from .entity import Entity as Entity
from .entity_component import EntityComponent as EntityComponent
from .entity_platform import EntityPlatform as EntityPlatform, async_get_platforms as async_get_platforms
from .service import async_register_admin_service as async_register_admin_service
from .typing import ConfigType as ConfigType
from _typeshed import Incomplete
from collections.abc import Iterable
from homeassistant.const import SERVICE_RELOAD as SERVICE_RELOAD
from homeassistant.core import HomeAssistant as HomeAssistant, ServiceCall as ServiceCall, callback as callback
from homeassistant.exceptions import HomeAssistantError as HomeAssistantError
from homeassistant.loader import async_get_integration as async_get_integration
from homeassistant.setup import async_setup_component as async_setup_component
from typing import Any, Literal, overload

_LOGGER: Incomplete
PLATFORM_RESET_LOCK: str

async def async_reload_integration_platforms(hass: HomeAssistant, integration_domain: str, platform_domains: Iterable[str]) -> None: ...
async def _resetup_platform(hass: HomeAssistant, integration_domain: str, platform_domain: str, unprocessed_config: ConfigType) -> None: ...
async def _async_setup_platform(hass: HomeAssistant, integration_domain: str, platform_domain: str, platform_configs: list[dict[str, Any]]) -> None: ...
async def _async_reconfig_platform(platform: EntityPlatform, platform_configs: list[dict[str, Any]]) -> None: ...
@overload
async def async_integration_yaml_config(hass: HomeAssistant, integration_name: str) -> ConfigType | None: ...
@overload
async def async_integration_yaml_config(hass: HomeAssistant, integration_name: str, *, raise_on_failure: Literal[True]) -> ConfigType: ...
@overload
async def async_integration_yaml_config(hass: HomeAssistant, integration_name: str, *, raise_on_failure: Literal[False] | bool) -> ConfigType | None: ...
def async_get_platform_without_config_entry(hass: HomeAssistant, integration_name: str, integration_platform_name: str) -> EntityPlatform | None: ...
async def async_setup_reload_service(hass: HomeAssistant, domain: str, platforms: Iterable[str]) -> None: ...
def setup_reload_service(hass: HomeAssistant, domain: str, platforms: Iterable[str]) -> None: ...
