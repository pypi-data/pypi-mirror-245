# THIS FILE IS GENERATED FROM github.com/GetStream/protocol/tree/main/openapi-gen/templates/python/type.tmpl
from dataclasses import dataclass, field
from dataclasses_json import config, dataclass_json

from datetime import datetime
from dateutil.parser import parse
from marshmallow import fields
from getstream.models.api_error import ApiError


@dataclass_json
@dataclass
class ConnectionErrorEvent:
    created_at: datetime = field(
        metadata=config(
            field_name="created_at",
            encoder=lambda d: d.isoformat(),
            decoder=parse,
            mm_field=fields.DateTime(format="iso"),
        )
    )
    error: ApiError = field(metadata=config(field_name="error"))
    type: str = field(metadata=config(field_name="type"))
    connection_id: str = field(metadata=config(field_name="connection_id"))
