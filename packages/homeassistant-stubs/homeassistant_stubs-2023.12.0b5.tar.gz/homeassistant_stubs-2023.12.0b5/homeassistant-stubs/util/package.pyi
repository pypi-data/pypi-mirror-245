from _typeshed import Incomplete

_LOGGER: Incomplete

def is_virtual_env() -> bool: ...
def is_docker_env() -> bool: ...
def is_installed(package: str) -> bool: ...
def install_package(package: str, upgrade: bool = ..., target: str | None = ..., constraints: str | None = ..., timeout: int | None = ...) -> bool: ...
async def async_get_user_site(deps_dir: str) -> str: ...
