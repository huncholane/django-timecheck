from dataclasses import dataclass
from environs import env as e
from django.conf import settings

from plusrequest.types import MissingAction


def env(type: str, key: str, default: str):
    return getattr(e, str(type))(f"PLUSREQUEST_{key}", default)


@dataclass()
class PlusRequestConf:
    """Dataclass for configuring PlusRequest"""

    header_timestamp_field: str = env("str", "HEADER_TIMESTAMP_FIELD", "lastUpdated")
    """Field in headers to use for client timestamp"""
    body_timestamp_field: str = env("str", "BODY_TIMESTAMP_FIELD", "lastUpdated")
    """Field in request body to use for client timestamp"""
    instance_timestamp_field: str = env(
        "str", "INSTANCE_TIMESTAMP_FIELD", "lastUpdated"
    )
    """Field in model instance to use for server timestamp"""
    noupdate_code: str = env("str", "NOUPDATE_CODE", "418")
    """Status code for when the client is newer on a GET or client is older on a POST"""
    missing_action: MissingAction = env("str", "MISSING_ACTION", "noupdate")
    """What do do when the client does not provide a timestamp"""
    datetime_format: str = env("str", "DATETIME_FORMAT", "%Y-%m-%dT%H:%M:%S%z")


if hasattr(settings, "PLUSREQUEST_CONF"):
    conf: PlusRequestConf = settings.PLUSREQUEST_CONF
else:
    conf = PlusRequestConf()
