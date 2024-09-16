from datetime import datetime, timezone
from functools import lru_cache
from typing import Literal, overload
from uuid import uuid4

from environs import Env


@lru_cache(maxsize=1)
def get_env():
    env = Env()
    env.read_env()
    return env


def generate_uuid(hexadecimal: bool = False):
    uuid = uuid4()
    if hexadecimal:
        return uuid.hex
    return str(uuid)


@overload
def utc_timestamp(unix: Literal[True]) -> int: ...


@overload
def utc_timestamp(unix: Literal[False]) -> datetime: ...


def utc_timestamp(unix: bool = False):
    utc_now = datetime.now(tz=timezone.utc)
    if unix:
        utc_now = int(utc_now.timestamp())
    return utc_now
