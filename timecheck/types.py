from typing import Literal, TypedDict

MissingAction = Literal["continue", "noupdate"]


class TimeCheckConf(TypedDict):
    """Dataclass for configuring TimeCheck"""

    header_field: str
    """Field in headers to use for client timestamp"""
    body_field: str
    """Field in request body to use for client timestamp"""
    instance_field: str
    """Field in model instance to use for server timestamp"""
    noupdate_code: int
    """Status code for when the client is newer on a GET or client is older on a POST"""
    missing_action: MissingAction
    """What do do when the client does not provide a timestamp"""
    dt_fmt: str
    """Format used to normalize datetimes."""
