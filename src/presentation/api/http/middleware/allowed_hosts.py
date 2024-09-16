from django.conf import settings
from fastapi.middleware.trustedhost import TrustedHostMiddleware

allowed_hosts_middleware_configuration = {
    "middleware_class": TrustedHostMiddleware,
    "allowed_hosts": settings.ALLOWED_HOSTS,
}
