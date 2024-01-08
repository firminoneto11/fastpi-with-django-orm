from functools import lru_cache
from typing import TYPE_CHECKING, Optional
from uuid import uuid4

from environs import Env

from .exceptions import EntityNotFoundError

if TYPE_CHECKING:
    from django.db.models import Model


def generate_uuid():
    return str(uuid4())


@lru_cache(maxsize=1)
def get_env():
    env = Env()
    env.read_env()
    return env


async def get_object_or_404[M: "Model"](
    model_class: type[M], exc_message: Optional[str] = None, *args, **kwargs
):
    try:
        return await model_class.objects.aget(**kwargs)
    except model_class.DoesNotExist as exc:
        raise EntityNotFoundError(detail=exc_message or "Object not found") from exc


def reverse_url(controller_name: str, *args, **kwargs):
    from conf.gateways.fastapi import application

    return application.url_path_for(controller_name, **kwargs)
