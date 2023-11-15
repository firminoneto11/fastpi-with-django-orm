from functools import lru_cache

from environs import Env


@lru_cache(maxsize=1)
def get_env():
    env = Env()
    env.read_env()
    return env
