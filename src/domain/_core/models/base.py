from typing import TYPE_CHECKING, Any, Self

from django.db import models
from django.utils.timezone import now

from shared.utils import generate_uuid_v7

if TYPE_CHECKING:
    from pydantic import BaseModel

    type UpdateData = BaseModel | dict[str, Any]


class BaseManager[M: models.Model](models.Manager[M]):
    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)


class TimeStampedBaseModel(models.Model):
    objects = BaseManager[Self]()

    class Meta:
        abstract = True

    id = models.UUIDField(verbose_name="ID", primary_key=True, default=generate_uuid_v7)

    # TODO: Find out a way to place the subclass' fields here on a table level

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    deleted_at = models.DateTimeField(null=True)
    deleted = models.BooleanField(default=False)

    async def adelete(  # type: ignore
        self,
        soft: bool = True,
        using: Any = None,
        keep_parents: bool = False,
    ):
        if soft:
            # TODO: Emit signals
            # TODO: Cascade delete to related objects by updating their deleted_at and deleted  # noqa

            self.deleted = True
            self.deleted_at = now()
            return await self.asave()

        await super().adelete(using=using, keep_parents=keep_parents)

    async def update(self, data: "UpdateData", save: bool = True):
        to_update = data if isinstance(data, dict) else data.model_dump(mode="json")
        changed = False

        for key in to_update:
            if (key not in self._sys_fields) and (hasattr(self, key)):
                current_value, new_value = getattr(self, key), to_update[key]

                # TODO: How to deal with data that is not that simple to compare? Eg:
                # relationships and concrete objects
                if current_value != new_value:
                    setattr(self, key, new_value)
                    changed = True

        if changed and save:
            await self.asave()

        return changed

    @property
    def _sys_fields(self):
        return {
            "pk_id",
            "id",
            "deleted",
            "created_at",
            "updated_at",
            "deleted_at",
        }
