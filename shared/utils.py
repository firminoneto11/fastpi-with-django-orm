from datetime import datetime, timezone
from functools import lru_cache
from typing import Literal, overload
from uuid import UUID, uuid4

from environs import Env


@overload
def generate_uuid(hexa: Literal[True]) -> str: ...


@overload
def generate_uuid(hexa: Literal[False]) -> UUID: ...


def generate_uuid(hexa: bool = False):
    uuid = uuid4()
    if hexa:
        return uuid.hex
    return uuid


@overload
def utc_timestamp(unix: Literal[True]) -> int: ...


@overload
def utc_timestamp(unix: Literal[False]) -> datetime: ...


def utc_timestamp(unix: bool = False):
    utc_now = datetime.now(tz=timezone.utc)
    if unix:
        utc_now = int(utc_now.timestamp())
    return utc_now


@lru_cache(maxsize=1)
def get_env():
    env = Env()
    env.read_env()
    return env
