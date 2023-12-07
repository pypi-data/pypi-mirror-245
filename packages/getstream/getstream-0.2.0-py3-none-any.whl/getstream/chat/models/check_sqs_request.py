# THIS FILE IS GENERATED FROM github.com/GetStream/protocol/tree/main/openapi-gen/templates/python/type.tmpl
from dataclasses import dataclass, field
from dataclasses_json import config, dataclass_json

from typing import Optional


@dataclass_json
@dataclass
class CheckSqsrequest:
    sqs_key: Optional[str] = field(metadata=config(field_name="sqs_key"), default=None)
    sqs_secret: Optional[str] = field(
        metadata=config(field_name="sqs_secret"), default=None
    )
    sqs_url: Optional[str] = field(metadata=config(field_name="sqs_url"), default=None)
