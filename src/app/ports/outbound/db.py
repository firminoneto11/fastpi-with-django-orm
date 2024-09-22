from abc import ABCMeta, abstractmethod


class DBPort(metaclass=ABCMeta):
    @abstractmethod
    async def ping(self, raise_exc: bool = False) -> bool: ...
