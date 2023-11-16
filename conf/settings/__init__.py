from importlib import import_module as _import_module

from shared.env import get_env as _get_env

_module = _get_env().str("ENVIRONMENT", "development").lower().strip()

if _module not in ("production", "staging", "development", "test"):
    raise RuntimeError(f"Invalid environment: {_module!r}")

_settings = _import_module(f"{__name__}.{_module}")

for variable in _settings.__dict__:
    if (not variable.startswith("__")) and (not variable.startswith("_")):
        globals()[variable] = _settings.__dict__[variable]
