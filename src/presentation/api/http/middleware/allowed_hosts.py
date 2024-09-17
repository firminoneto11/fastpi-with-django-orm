from typing import TYPE_CHECKING

from fastapi.middleware.trustedhost import TrustedHostMiddleware

if TYPE_CHECKING:
    from django.conf import LazySettings


def get_allowed_hosts_config(settings: "LazySettings"):
    return {
        "middleware_class": TrustedHostMiddleware,
        "allowed_hosts": settings.ALLOWED_HOSTS,
    }
