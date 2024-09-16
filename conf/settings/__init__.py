from importlib import import_module as _import_module
from typing import cast

from shared.utils import get_env as _get_env

from . import base

_ALLOWED_ENVIRONMENTS = ("production", "staging", "development", "testing")

with _get_env().prefixed(base.ENVIRONMENT_PREFIX) as _env:
    _module = cast(str, _env.str("ENVIRONMENT", "development")).lower().strip()  # type: ignore

if _module not in _ALLOWED_ENVIRONMENTS:
    raise RuntimeError(f"Invalid environment: {_module!r}")

_settings = _import_module(f"{__name__}.{_module}")

for variable in _settings.__dict__:
    cond = (not variable.startswith("__")) and (not variable.startswith("_"))
    if (cond) and (variable not in globals()):
        globals()[variable] = _settings.__dict__[variable]
