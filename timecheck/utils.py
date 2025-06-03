import datetime as dt
from rest_framework import serializers

from timecheck.settings import conf


def parse_dt(s: str):
    return serializers.DateTimeField().to_internal_value(s)


def normalize_dt(t: dt.datetime, fmt=conf["dt_fmt"]):
    return dt.datetime.strptime(t.strftime(fmt), fmt)
