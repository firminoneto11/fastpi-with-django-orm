from typing import TYPE_CHECKING, Any, Self, cast

from django.db import models
from django.utils.timezone import now

from shared.utils import generate_uuid

if TYPE_CHECKING:
    from pydantic import BaseModel

    type UpdateData = BaseModel | dict[str, Any]


class BaseManager[M: models.Model](models.Manager[M]):
    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)

    def retrieve_deleted(self):
        return super().get_queryset()


class TimeStampedBaseModel(models.Model):
    objects = BaseManager[Self]()

    class Meta:
        abstract = True

    pk_id = cast(int, models.BigAutoField(primary_key=True))
    id = models.CharField(unique=True, default=generate_uuid, max_length=36)

    deleted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)

    async def adelete(self):  # type: ignore
        # TODO: Emit signals
        # TODO: Cascade delete to related objects by updating their deleted_at and deleted  # noqa

        self.deleted = True
        self.deleted_at = now()
        await self.asave()

    async def hard_delete(self, using: Any = None, keep_parents: bool = False):
        await super().adelete(using=using, keep_parents=keep_parents)

    async def update(self, data: "UpdateData", save: bool = True):
        to_update = data if isinstance(data, dict) else data.model_dump(mode="json")
        editable_fields, changed = self._get_editable_fields(), False

        for key in to_update:
            if key in editable_fields:
                current_value, new_value = getattr(self, key), to_update[key]
                changed = current_value != new_value
                setattr(self, key, new_value)

                # TODO: How to deal with data that is not that simple to compare? Eg:
                # relationships and concrete objects

        if changed and save:
            await self.asave()

        return self

    @classmethod
    def _get_editable_fields(cls):
        SYS_FIELDS = {
            "pk_id",
            "id",
            "deleted",
            "created_at",
            "updated_at",
            "deleted_at",
        }
        return {
            cast(str, field.name)
            for field in cls._meta.fields
            if field.name not in SYS_FIELDS
        }
