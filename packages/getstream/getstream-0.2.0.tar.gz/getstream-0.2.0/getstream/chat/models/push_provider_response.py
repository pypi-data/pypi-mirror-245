# THIS FILE IS GENERATED FROM github.com/GetStream/protocol/tree/main/openapi-gen/templates/python/type.tmpl
from dataclasses import dataclass, field
from dataclasses_json import config, dataclass_json

from typing import Optional
from datetime import datetime
from dateutil.parser import parse
from marshmallow import fields


@dataclass_json
@dataclass
class PushProviderResponse:
    name: str = field(metadata=config(field_name="name"))
    updated_at: datetime = field(
        metadata=config(
            field_name="updated_at",
            encoder=lambda d: d.isoformat(),
            decoder=parse,
            mm_field=fields.DateTime(format="iso"),
        )
    )
    type: str = field(metadata=config(field_name="type"))
    created_at: datetime = field(
        metadata=config(
            field_name="created_at",
            encoder=lambda d: d.isoformat(),
            decoder=parse,
            mm_field=fields.DateTime(format="iso"),
        )
    )
    apn_topic: Optional[str] = field(
        metadata=config(field_name="apn_topic"), default=None
    )
    firebase_server_key: Optional[str] = field(
        metadata=config(field_name="firebase_server_key"), default=None
    )
    huawei_app_secret: Optional[str] = field(
        metadata=config(field_name="huawei_app_secret"), default=None
    )
    huawei_app_id: Optional[str] = field(
        metadata=config(field_name="huawei_app_id"), default=None
    )
    firebase_credentials: Optional[str] = field(
        metadata=config(field_name="firebase_credentials"), default=None
    )
    apn_development: Optional[bool] = field(
        metadata=config(field_name="apn_development"), default=None
    )
    apn_host: Optional[str] = field(
        metadata=config(field_name="apn_host"), default=None
    )
    apn_p_12_cert: Optional[str] = field(
        metadata=config(field_name="apn_p12_cert"), default=None
    )
    firebase_apn_template: Optional[str] = field(
        metadata=config(field_name="firebase_apn_template"), default=None
    )
    firebase_notification_template: Optional[str] = field(
        metadata=config(field_name="firebase_notification_template"), default=None
    )
    apn_auth_type: Optional[str] = field(
        metadata=config(field_name="apn_auth_type"), default=None
    )
    apn_supports_voip_notifications: Optional[bool] = field(
        metadata=config(field_name="apn_supports_voip_notifications"), default=None
    )
    xiaomi_package_name: Optional[str] = field(
        metadata=config(field_name="xiaomi_package_name"), default=None
    )
    apn_supports_remote_notifications: Optional[bool] = field(
        metadata=config(field_name="apn_supports_remote_notifications"), default=None
    )
    disabled_at: Optional[datetime] = field(
        metadata=config(
            field_name="disabled_at",
            encoder=lambda d: d.isoformat() if d is not None else None,
            decoder=parse,
            mm_field=fields.DateTime(format="iso"),
        ),
        default=None,
    )
    apn_auth_key: Optional[str] = field(
        metadata=config(field_name="apn_auth_key"), default=None
    )
    apn_key_id: Optional[str] = field(
        metadata=config(field_name="apn_key_id"), default=None
    )
    apn_sandbox_certificate: Optional[bool] = field(
        metadata=config(field_name="apn_sandbox_certificate"), default=None
    )
    description: Optional[str] = field(
        metadata=config(field_name="description"), default=None
    )
    xiaomi_app_secret: Optional[str] = field(
        metadata=config(field_name="xiaomi_app_secret"), default=None
    )
    disabled_reason: Optional[str] = field(
        metadata=config(field_name="disabled_reason"), default=None
    )
    firebase_data_template: Optional[str] = field(
        metadata=config(field_name="firebase_data_template"), default=None
    )
    firebase_host: Optional[str] = field(
        metadata=config(field_name="firebase_host"), default=None
    )
    apn_team_id: Optional[str] = field(
        metadata=config(field_name="apn_team_id"), default=None
    )
