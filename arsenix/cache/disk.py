try:
    from diskcache import Cache
except ImportError:
    Cache = None

class DiskCache:
    """A file-based cache that uses the `diskcache` library for persistence."""
    def __init__(self, directory='cache'):
        """Initializes the disk cache.

        Args:
            directory (str, optional): The path to the directory where the cache will be stored.
                                       Defaults to 'cache'.

        Raises:
            ImportError: If the `diskcache` library is not installed.
        """
        if Cache is None:
            raise ImportError("diskcache is not installed. Please run: pip install arsenix[diskcache]")
        self._cache = Cache(directory)

    async def get(self, key, default=None):
        """Asynchronously retrieves an item from the disk cache by its key.

        Args:
            key (any): The key of the item to retrieve.
            default (any, optional): The default value to return if the key is not found.

        Returns:
            The value associated with the key, or the default value.
        """
        return self._cache.get(key, default=default)

    async def put(self, key, value):
        """Asynchronously adds an item to the disk cache.

        If the key already exists, its value will be overwritten.

        Args:
            key (any): The key of the item to store.
            value (any): The value to be stored.
        """
        self._cache.set(key, value)

    async def delete(self, key):
        """Asynchronously removes an item from the disk cache by its key.

        Args:
            key (any): The key of the item to remove.

        Returns:
            bool: True if the item was successfully removed, False if the key was not found.
        """
        return self._cache.delete(key)

    async def clear(self):
        """Asynchronously clears the entire disk cache, removing all items."""
        self._cache.clear()
