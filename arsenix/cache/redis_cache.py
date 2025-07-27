import pickle

try:
    import redis.asyncio as redis
except ImportError:
    redis = None

class RedisCache:
    """A cache that uses Redis as a backend for storing key-value pairs."""
    def __init__(self, url='redis://localhost:6379'):
        """Initializes the Redis cache.

        Args:
            url (str, optional): The connection URL for the Redis server.
                                 Defaults to 'redis://localhost:6379'.

        Raises:
            ImportError: If the `redis` library is not installed.
        """
        if redis is None:
            raise ImportError("redis is not installed. Please run: pip install arsenix[redis]")
        self._redis = redis.from_url(url)

    async def get(self, key, default=None):
        """Asynchronously retrieves an item from the Redis cache by its key.

        Args:
            key (any): The key of the item to retrieve.
            default (any, optional): The default value to return if the key is not found.

        Returns:
            The deserialized value associated with the key, or the default value.
        """
        value = await self._redis.get(key)
        return pickle.loads(value) if value else default

    async def put(self, key, value):
        """Asynchronously adds a serialized item to the Redis cache.

        If the key already exists, its value will be overwritten.

        Args:
            key (any): The key of the item to store.
            value (any): The value to be stored (will be pickled).
        """
        await self._redis.set(key, pickle.dumps(value))

    async def delete(self, key):
        """Asynchronously removes an item from the Redis cache by its key.

        Args:
            key (any): The key of the item to remove.

        Returns:
            int: The number of keys that were removed (0 or 1).
        """
        return await self._redis.delete(key)

    async def clear(self):
        """Asynchronously clears the entire Redis database.

        Warning:
            This will delete all keys in the current Redis database, not just those
            created by this cache instance.
        """
        await self._redis.flushdb()
