from functools import lru_cache
from uuid import uuid4

from environs import Env


def generate_uuid():
    return str(uuid4())


@lru_cache(maxsize=1)
def get_env():
    env = Env()
    env.read_env()
    return env
