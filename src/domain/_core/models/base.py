from typing import TYPE_CHECKING, Any, Self

import pgtrigger
from asgiref.sync import sync_to_async
from django.db import models
from django.db.transaction import atomic as initiate_transaction
from django.utils.timezone import now

from shared.utils import generate_uuid_v7

models.OneToOneRel
if TYPE_CHECKING:
    from pydantic import BaseModel

    type UpdateData = BaseModel | dict[str, Any]


@sync_to_async
def _cascade_soft_deletion(parent: "TimeStampedBaseModel"):
    with initiate_transaction():
        for field in parent._meta.get_fields(include_hidden=True):
            should_cascade = (field.one_to_many or field.one_to_one) and (
                field.auto_created and (not field.concrete)
            )
            if should_cascade:
                get_manager = getattr(parent, field.get_accessor_name, None)  # type: ignore

                related_manager = (  # type: ignore
                    get_manager() if callable(get_manager) else None  # type: ignore
                )

                if related_manager:
                    related_manager.all().update(  # type: ignore
                        deleted=parent.deleted,
                        deleted_at=parent.deleted_at,
                    )


class FilterDeletedManager[M: models.Model](models.Manager[M]):
    def get_queryset(self):
        return super().get_queryset().exclude(deleted=True).exclude(is_active=False)


class TimeStampedBaseModel(models.Model):
    objects = FilterDeletedManager[Self]()
    _all_objects = models.Manager[Self]()

    class Meta:
        abstract = True
        default_manager_name = "_all_objects"
        triggers = [
            pgtrigger.SoftDelete(name="soft_delete", field="is_active", value=False),
        ]

    id = models.UUIDField(verbose_name="ID", primary_key=True, default=generate_uuid_v7)

    # TODO: Find out a way to place the subclass' fields here on a table level

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    deleted_at = models.DateTimeField(null=True)
    deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    models.ForeignKey
    models.OneToOneField

    # async def adelete(  # type: ignore
    #     self,
    #     soft: bool = True,
    #     using: Any = None,
    #     keep_parents: bool = False,
    # ):
    #     if soft:
    #         # TODO: Emit signals

    #         self.deleted = True
    #         self.deleted_at = now()

    #         await _cascade_soft_deletion(parent=self)
    #         return await self.asave()

    #     await super().adelete(using=using, keep_parents=keep_parents)

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
