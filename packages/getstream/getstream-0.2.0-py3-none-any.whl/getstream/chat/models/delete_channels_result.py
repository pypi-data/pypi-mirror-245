# THIS FILE IS GENERATED FROM github.com/GetStream/protocol/tree/main/openapi-gen/templates/python/type.tmpl
from dataclasses import dataclass, field
from dataclasses_json import config, dataclass_json

from typing import Optional


@dataclass_json
@dataclass
class DeleteChannelsResult:
    status: str = field(metadata=config(field_name="status"))
    error: Optional[str] = field(metadata=config(field_name="error"), default=None)
