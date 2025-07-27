class LocalCache:
    def __init__(self):
        self._cache = {}

    async def get(self, key, default=None):
        """Retrieves an item from the cache."""
        return self._cache.get(key, default)

    async def put(self, key, value):
        """Adds an item to the cache."""
        self._cache[key] = value

    async def delete(self, key):
        """Removes an item from the cache. Returns True if successful, False otherwise."""
        if key in self._cache:
            del self._cache[key]
            return True
        return False

    async def clear(self):
        """Clears the entire cache."""
        self._cache.clear()
