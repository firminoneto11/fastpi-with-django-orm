from django.db import models

from shared.models import TimeStampedBaseModel


class Product(TimeStampedBaseModel):
    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    name = models.CharField(max_length=255)
