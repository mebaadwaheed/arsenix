class ARGetter:
    """Handles retrieving data from the main data store."""
    def __init__(self, data_store):
        """Initializes the getter with a reference to the data store.

        Args:
            data_store (dict): The data store to retrieve from.
        """
        if not isinstance(data_store, dict):
            raise TypeError("data_store must be a dictionary.")
        self.data_store = data_store

    async def get(self, key, default=None):
        """Asynchronously retrieves a value from the data store by its key.

        Args:
            key (any): The key of the item to retrieve.
            default (any, optional): The default value to return if the key is not found.

        Returns:
            The value associated with the key, or the default value.
        """
        return self.data_store.get(key, default)