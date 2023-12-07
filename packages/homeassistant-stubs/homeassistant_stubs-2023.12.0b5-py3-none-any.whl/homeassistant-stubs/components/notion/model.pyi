from aionotion.sensor.models import ListenerKind as ListenerKind
from dataclasses import dataclass

@dataclass
class NotionEntityDescriptionMixin:
    listener_kind: ListenerKind
    def __init__(self, listener_kind) -> None: ...
