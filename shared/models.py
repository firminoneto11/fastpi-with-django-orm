from typing import TYPE_CHECKING, Any, TypeVar
from uuid import uuid4

from asgiref.sync import sync_to_async
from django.db import models
from django.utils.timezone import now

if TYPE_CHECKING:
    from pydantic import BaseModel

    UpdateModel = TypeVar("UpdateModel", BaseModel, dict[str, Any])


def generate_uuid():
    return uuid4().hex


class BaseManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)

    def default_queryset(self):
        return super().get_queryset()


class TimeStampedBaseModel(models.Model):
    class Meta:
        abstract = True

    id = models.CharField(
        primary_key=True, unique=True, default=generate_uuid, max_length=32
    )
    deleted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)

    objects = BaseManager()

    async def adelete(self):
        self.deleted = True
        self.deleted_at = now()
        # TODO: Emit signals
        await self.asave()

    async def _hard_delete(self, *args, **kwargs):
        await super().adelete(*args, **kwargs)

    async def update(self, data: "UpdateModel", save: bool = False):
        to_update = data if isinstance(data, dict) else data.model_dump(mode="json")
        editable_fields, changed = self._editable_fields(), False

        for key in to_update:
            if key in editable_fields:
                current_value, new_value = getattr(self, key), to_update[key]
                if current_value != new_value:
                    setattr(self, key, new_value)
                    changed = True

        if changed and save:
            await self.asave()

    @classmethod
    def _editable_fields(cls) -> set[str]:
        SYS_FIELDS = ("id", "deleted", "created_at", "updated_at", "deleted_at")
        return {
            field.name for field in cls._meta.fields if field.name not in SYS_FIELDS
        }

    @classmethod
    async def fetch_all(cls):
        func = lambda: list(cls.objects.all())  # noqa
        return await sync_to_async(func)()
