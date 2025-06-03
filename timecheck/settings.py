from typing import Any
from environs import env
from django.conf import settings

from timecheck.types import TimeCheckConf


def e(type: type, key: str, default: str):
    return getattr(env, type.__name__)(f"TIMECHECK_{key.upper()}", default)


initial = getattr(settings, "TIMECHECK_CONF", {})


def getval(t: type, k: str, d: Any):
    return initial.get(k, e(t, k, d))


conf = TimeCheckConf(
    {
        "body_timestamp_field": getval(str, "body_timestamp_field", "lastUpdated"),
        "datetime_format": getval(str, "datetime_format", "%Y-%m-%dT%H:%M:%S%z"),
        "header_timestamp_field": getval(str, "header_timestamp_field", "lastUpdated"),
        "instance_timestamp_field": getval(
            str, "instance_timestamp_field", "lastUpdated"
        ),
        "missing_action": getval(str, "missing_action", "noupdate"),
        "noupdate_code": getval(int, "noupdate_code", 418),
        "replace_with_z": getval(bool, "replace_with_z", True),
    }
)
