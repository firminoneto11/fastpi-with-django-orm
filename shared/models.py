from typing import TYPE_CHECKING, Any, Self

from asgiref.sync import sync_to_async
from django.db import models
from django.utils.timezone import now

from .utils import generate_uuid

if TYPE_CHECKING:
    from pydantic import BaseModel

    type UpdateData = BaseModel | dict[str, Any]


class BaseManager[M: models.Model](models.Manager[M]):
    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)

    def with_deleted(self):
        return super().get_queryset()

    async def fetch_qs(self, qs: models.QuerySet[M]):
        return await sync_to_async(lambda: list(qs))()


class TimeStampedBaseModel(models.Model):
    class Meta:
        abstract = True

    pk_id: int = models.BigAutoField(primary_key=True)
    id = models.CharField(unique=True, default=generate_uuid, max_length=36)

    deleted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)

    objects: BaseManager[Self] = BaseManager()

    async def adelete(self):
        self.deleted = True
        self.deleted_at = now()
        # TODO: Emit signals
        # TODO: Cascade delete to related objects by updating their deleted_at and deleted  # noqa
        await self.asave()

    async def hard_delete(self, *args, **kwargs):
        await super().adelete(*args, **kwargs)

    async def update(self, data: "UpdateData", save: bool = True):
        to_update = data if isinstance(data, dict) else data.model_dump(mode="json")
        editable_fields, changed = self._get_editable_fields(), False

        for key in to_update:
            if key in editable_fields:  # pragma: no branch
                current_value, new_value = getattr(self, key), to_update[key]
                changed = current_value != new_value
                setattr(self, key, new_value)

        if changed and save:  # pragma: no branch
            await self.asave()

        return self

    @classmethod
    def _get_editable_fields(cls) -> set[str]:
        SYS_FIELDS = {
            "pk_id",
            "id",
            "deleted",
            "created_at",
            "updated_at",
            "deleted_at",
        }
        return {
            field.name for field in cls._meta.fields if field.name not in SYS_FIELDS
        }
