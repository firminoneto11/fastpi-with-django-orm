from importlib import import_module
from typing import cast

from shared.utils import get_env

from .base import ALLOWED_ENVIRONMENTS, ENVIRONMENT_PREFIX

with get_env().prefixed(ENVIRONMENT_PREFIX) as _env:
    module = cast(str, _env.str("ENVIRONMENT", "development")).lower().strip()  # type: ignore

if module not in ALLOWED_ENVIRONMENTS:
    raise RuntimeError(f"Invalid environment: {module!r}")

settings = import_module(f"{__name__}.{module}")

for variable in settings.__dict__:
    cond = (
        (not variable.startswith("__"))
        and (not variable.startswith("_"))
        and (variable.isupper())
    )
    if (cond) and (variable not in globals()):
        globals()[variable] = settings.__dict__[variable]
