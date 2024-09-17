from django.db import models

from .base import TimeStampedBaseModel


class Product(TimeStampedBaseModel):
    class Meta:  # type: ignore
        verbose_name = "Product"
        verbose_name_plural = "Products"

    name = models.CharField(max_length=255)
