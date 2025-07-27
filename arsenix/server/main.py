from ..setup import ARGetter, ARSetter
from ..cache import LocalCache
from ..pattern import Pattern

class ArsenixServer:
    def __init__(self, data_store=None):
        if data_store is None:
            data_store = {}
        
        self.data_store = data_store
        self.getter = ARGetter(self.data_store)
        self.setter = ARSetter(self.data_store)
        self.cache = LocalCache()
        self.pattern = Pattern()

    async def get(self, key, default=None):
        return await self.getter.get(key, default)

    async def set(self, key, value):
        return await self.setter.set(key, value)

    async def load_from_file(self, filepath):
        return await self.setter.load_from_file(filepath)
