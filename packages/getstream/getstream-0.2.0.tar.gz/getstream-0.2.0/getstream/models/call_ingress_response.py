# THIS FILE IS GENERATED FROM github.com/GetStream/protocol/tree/main/openapi-gen/templates/python/type.tmpl
from dataclasses import dataclass, field
from dataclasses_json import config, dataclass_json

from getstream.models.rtmp_ingress import Rtmpingress


@dataclass_json
@dataclass
class CallIngressResponse:
    rtmp: Rtmpingress = field(metadata=config(field_name="rtmp"))
