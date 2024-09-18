from adrf.serializers import ModelSerializer  # type: ignore
from asgiref.sync import sync_to_async


class BaseAsyncModelSerializer(ModelSerializer):
    async def async_is_valid(self, raise_exception: bool = False):
        return await sync_to_async(self.is_valid)(raise_exception=raise_exception)
