from uuid import uuid4

from asgiref.sync import sync_to_async
from django.db import models
from django.utils.timezone import now


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

    async def adelete(self, *args, **kwargs):
        self.deleted = True
        self.deleted_at = now()
        # Should we emit signals?
        await self.asave(*args, **kwargs)

    async def _hard_delete(self, *args, **kwargs):
        await super().adelete(*args, **kwargs)

    @classmethod
    async def fetch_all(cls):
        func = lambda: list(cls.objects.all())  # noqa
        return await sync_to_async(func)()
