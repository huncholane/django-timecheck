import datetime as dt
from rest_framework import serializers

from timecheck.settings import conf


def parse_dt(s: str):
    return serializers.DateTimeField().to_internal_value(s)


def fmt_dt(
    time: dt.datetime,
    fmt: str = conf["datetime_format"],
    replace_with_z=conf["replace_with_z"],
):
    s = dt.datetime.strftime(time, fmt)
    if replace_with_z:
        return s.replace("+0000", "Z")
    return s


def normalize_dt(t: dt.datetime, fmt=conf["datetime_format"]):
    return dt.datetime.strptime(t.strftime(fmt), fmt)
