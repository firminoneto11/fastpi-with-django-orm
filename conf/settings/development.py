from .base import *  # noqa


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "database.db",  # noqa
    }
}

DEBUG = True

ALLOWED_HOSTS = ["*"]
