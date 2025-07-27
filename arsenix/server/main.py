from ..setup import ARGetter, ARSetter
from ..cache import LocalCache, DiskCache, RedisCache
from ..pattern import Pattern
from ..algorithm import FYPBuilder

class ArsenixServer:
    """The main server class for ArsenixPY, providing a unified interface for all features."""
    def __init__(self, data_store=None):
        """Initializes the ArsenixServer.

        Args:
            data_store (dict, optional): An initial dictionary to populate the data store.
                                       If not provided, an empty store is created.
        """
        if data_store is None:
            data_store = {}
        
        self.data_store = data_store
        self.getter = ARGetter(self.data_store)
        self.setter = ARSetter(self.data_store)
        self.cache = LocalCache()
        self.pattern = Pattern()

    async def get(self, key, default=None):
        """Retrieves a value from the data store by its key.

        Args:
            key (any): The key of the item to retrieve.
            default (any, optional): The default value to return if the key is not found.

        Returns:
            The value associated with the key, or the default value.
        """
        return await self.getter.get(key, default)

    async def set(self, key, value):
        """Sets a key-value pair in the data store.

        Args:
            key (any): The key of the item to set.
            value (any): The value to store.
        """
        return await self.setter.set(key, value)

    async def load_from_file(self, filepath):
        """Loads the data store from a JSON or YAML file.

        Args:
            filepath (str): The path to the file to load.

        Returns:
            bool: True if the file was loaded successfully, False otherwise.
        """
        return await self.setter.load_from_file(filepath)

    async def sync(self, action, filepath='arsenix_store.json'):
        """Saves or loads the data store to/from a file.

        This method provides a high-level interface for persistence.

        Args:
            action (str): The action to perform. Must be 'save' or 'load'.
            filepath (str, optional): The path to the file. Defaults to 'arsenix_store.json'.

        Returns:
            bool: True on success, False on failure.
        """
        if action == 'save':
            return await self.setter.save_to_file(filepath)
        elif action == 'load':
            return await self.setter.load_from_file(filepath)
        else:
            raise ValueError("Invalid sync action. Use 'save' or 'load'.")

    def use_cache(self, provider, **kwargs):
        """Switches the caching engine dynamically.

        This allows you to plug in different caching backends like 'diskcache' or 'redis'.

        Args:
            provider (str): The cache provider to use. Supported values: 'diskcache', 'redis'.
            **kwargs: Connection arguments for the selected cache provider.
                      For 'diskcache', this can include `directory`.
                      For 'redis', this can include `url`.

        Raises:
            ImportError: If the required library for the provider is not installed.
        """
        if provider == 'diskcache':
            try:
                from diskcache import Cache
                self.cache = DiskCache(**kwargs)
            except ImportError:
                raise ImportError("diskcache is not installed. Please run: pip install arsenix[diskcache]")
        elif provider == 'redis':
            try:
                import redis.asyncio as redis
                self.cache = RedisCache(**kwargs)
            except ImportError:
                raise ImportError("redis is not installed. Please run: pip install arsenix[redis]")
        else:
            self.cache = LocalCache()

    async def get_recommendations(self, user_id, top_n=3, limit=10):
        """Generates personalized recommendations for a user.

        This method combines a user's learned interest patterns with the declarative
        FYPBuilder to produce a ranked list of recommended items.

        Args:
            user_id (any): The unique identifier for the user.
            top_n (int, optional): The number of top interests to use from the user's pattern.
                                 Defaults to 3.
            limit (int, optional): The maximum number of recommendations to return.
                                   Defaults to 10.

        Returns:
            list: A list of recommended items, sorted by relevance.
        """
        user_pattern = await self.pattern.get_pattern(user_id)
        if not user_pattern:
            return []

        interest_tags = [tag for tag, score in user_pattern.most_common(top_n)]

        builder = FYPBuilder(self.getter.data_store)
        recommendations = await builder.match_tags(interest_tags).sort_by('popularity', reverse=True).limit(limit).run()
        
        return recommendations

