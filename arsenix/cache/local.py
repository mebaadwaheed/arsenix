class LocalCache:
    """A simple in-memory cache for storing key-value pairs."""
    def __init__(self):
        """Initializes the local cache with an empty dictionary."""
        self._cache = {}

    async def get(self, key, default=None):
        """Asynchronously retrieves an item from the cache by its key.

        Args:
            key (any): The key of the item to retrieve.
            default (any, optional): The default value to return if the key is not found.

        Returns:
            The value associated with the key, or the default value.
        """
        return self._cache.get(key, default)

    async def put(self, key, value):
        """Asynchronously adds an item to the cache.

        If the key already exists, its value will be overwritten.

        Args:
            key (any): The key of the item to store.
            value (any): The value to be stored.
        """
        self._cache[key] = value

    async def delete(self, key):
        """Asynchronously removes an item from the cache by its key.

        Args:
            key (any): The key of the item to remove.

        Returns:
            bool: True if the item was successfully removed, False if the key was not found.
        """
        if key in self._cache:
            del self._cache[key]
            return True
        return False

    async def clear(self):
        """Asynchronously clears the entire cache, removing all items."""
        self._cache.clear()
