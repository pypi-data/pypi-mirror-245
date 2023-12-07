# THIS FILE IS GENERATED FROM github.com/GetStream/protocol/tree/main/openapi-gen/templates/python/type.tmpl
from dataclasses import dataclass, field
from dataclasses_json import config, dataclass_json

from typing import Optional
from getstream.chat.models.command import Command


@dataclass_json
@dataclass
class CreateCommandResponse:
    duration: str = field(metadata=config(field_name="duration"))
    command: Optional[Command] = field(
        metadata=config(field_name="command"), default=None
    )
