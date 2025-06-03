from typing import Literal, TypedDict

MissingAction = Literal["continue", "noupdate"]


class TimeCheckConf(TypedDict):
    """Dataclass for configuring TimeCheck"""

    header_timestamp_field: str
    """Field in headers to use for client timestamp"""
    body_timestamp_field: str
    """Field in request body to use for client timestamp"""
    instance_timestamp_field: str
    """Field in model instance to use for server timestamp"""
    noupdate_code: int
    """Status code for when the client is newer on a GET or client is older on a POST"""
    missing_action: MissingAction
    """What do do when the client does not provide a timestamp"""
    datetime_format: str
    replace_with_z: bool
