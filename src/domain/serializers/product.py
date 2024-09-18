from src.domain.models import Product

from .base import BaseAsyncModelSerializer


class ProductSerializer(BaseAsyncModelSerializer):
    class Meta:  # type: ignore
        model = Product
        fields = ["name", "price"]
