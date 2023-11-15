from .base import *  # noqa

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    },
}

DEBUG = True

ALLOWED_HOSTS = ["*"]

SOUTH_TESTS_MIGRATE = False
