# THIS FILE IS GENERATED FROM github.com/GetStream/protocol/tree/main/openapi-gen/templates/python/type.tmpl
from dataclasses import dataclass, field
from dataclasses_json import config, dataclass_json

from typing import Optional
from getstream.chat.models.event import Event


@dataclass_json
@dataclass
class EventResponse:
    duration: str = field(metadata=config(field_name="duration"))
    event: Optional[Event] = field(metadata=config(field_name="event"), default=None)
