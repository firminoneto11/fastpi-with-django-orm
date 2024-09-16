from .base import *  # noqa


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    },
}

DEBUG = True

ALLOWED_HOSTS = ["*"]

SOUTH_TESTS_MIGRATE = False
