class ARGetter:
    def __init__(self, data_store):
        if not isinstance(data_store, dict):
            raise TypeError("data_store must be a dictionary.")
        self.data_store = data_store

    async def get(self, key, default=None):
        """Retrieves a value by key from the data store."""
        return self.data_store.get(key, default)