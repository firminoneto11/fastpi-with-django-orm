from importlib import import_module as _import_module

from shared.env import get_env as _get_env

_settings = _import_module(
    f'{__name__}.{_get_env().str("ENVIRONMENT", "development").lower().strip()}'
)

for variable in _settings.__dict__:
    if not variable.startswith("__") or not variable.startswith("_"):
        globals()[variable] = _settings.__dict__[variable]
