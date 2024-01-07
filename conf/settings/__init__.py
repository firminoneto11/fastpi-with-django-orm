from importlib import import_module as _import_module

from shared.utils import get_env as _get_env

_allowed_environments = ("production", "staging", "development", "test")
_module = _get_env().str("ENVIRONMENT", "development").lower().strip()

if _module not in _allowed_environments:
    raise RuntimeError(f"Invalid environment: {_module!r}")

_settings = _import_module(f"{__name__}.{_module}")

for variable in _settings.__dict__:
    cond = (not variable.startswith("__")) and (not variable.startswith("_"))
    if (cond) and (variable not in globals()):  # pragma: no branch
        globals()[variable] = _settings.__dict__[variable]
