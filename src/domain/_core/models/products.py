from decimal import Decimal

from django.db import models

from .base import TimeStampedBaseModel


class Product(TimeStampedBaseModel):
    class Meta:  # type: ignore
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ("-id",)

    name = models.CharField(verbose_name="Name", max_length=255, unique=True)
    price = models.DecimalField(
        verbose_name="Price", max_digits=10, decimal_places=2, default=Decimal(0)
    )
