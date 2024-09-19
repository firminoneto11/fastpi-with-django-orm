from datetime import datetime, timezone
from functools import lru_cache
from typing import Literal, overload
from uuid import UUID

from environs import Env
from uuid_extensions import uuid7  # type: ignore


@overload
def generate_uuid_v7(as_string: Literal[True] = False) -> str: ...  # type: ignore


@overload
def generate_uuid_v7(as_string: Literal[False] = False) -> UUID: ...


def generate_uuid_v7(as_string: bool = False):
    uuid = uuid7()
    return str(uuid) if as_string else uuid


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
