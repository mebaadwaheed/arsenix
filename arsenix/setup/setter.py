import json
import yaml
import aiofiles

class ARSetter:
    """Handles modifying data in the main data store."""
    def __init__(self, data_store):
        """Initializes the setter with a reference to the data store.

        Args:
            data_store (dict): The data store to modify.
        """
        if not isinstance(data_store, dict):
            raise TypeError("data_store must be a dictionary.")
        self.data_store = data_store

    async def set(self, key, value):
        """Asynchronously sets or updates a key-value pair in the data store.

        Args:
            key (any): The key of the item to set.
            value (any): The value to store.

        Returns:
            bool: True on success.
        """
        self.data_store[key] = value
        return True

    async def update(self, key, new_value):
        """Asynchronously updates an existing entry.

        If the existing value and new value are both dictionaries, it performs a merge.
        Otherwise, it replaces the value.

        Args:
            key (any): The key of the item to update.
            new_value (any): The new value to set.

        Returns:
            bool: True if the update was successful, False if the key does not exist.
        """
        if key in self.data_store:
            if isinstance(self.data_store[key], dict) and isinstance(new_value, dict):
                self.data_store[key].update(new_value)
            else:
                self.data_store[key] = new_value
            return True
        return False

    async def delete(self, key):
        """Asynchronously deletes an entry from the data store by its key.

        Args:
            key (any): The key of the item to delete.

        Returns:
            bool: True if the deletion was successful, False if the key does not exist.
        """
        if key in self.data_store:
            del self.data_store[key]
            return True
        return False

    async def bulk_set(self, data):
        """Asynchronously adds multiple entries to the data store from a dictionary.

        Args:
            data (dict): A dictionary of key-value pairs to add.

        Returns:
            bool: True on success.

        Raises:
            TypeError: If the input data is not a dictionary.
        """
        if not isinstance(data, dict):
            raise TypeError("Input data must be a dictionary.")
        self.data_store.update(data)
        return True

    async def load_from_file(self, filepath):
        """Asynchronously loads data from a JSON or YAML file and adds it to the data store.

        Args:
            filepath (str): The path to the file to load.

        Returns:
            bool: True if the file was loaded and data was set successfully, False otherwise.
        """
        try:
            async with aiofiles.open(filepath, 'r') as f:
                content = await f.read()
                if filepath.endswith('.json'):
                    data = json.loads(content)
                elif filepath.endswith('.yaml') or filepath.endswith('.yml'):
                    data = yaml.safe_load(content)
                else:
                    raise ValueError("Unsupported file type. Please use JSON or YAML.")
            return await self.bulk_set(data)
        except FileNotFoundError:
            print(f"Error: File not found at {filepath}")
            return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    async def save_to_file(self, filepath):
        """Asynchronously saves the entire data store to a JSON or YAML file.

        Args:
            filepath (str): The path to the file to save.

        Returns:
            bool: True if the file was saved successfully, False otherwise.
        """
        try:
            async with aiofiles.open(filepath, 'w') as f:
                if filepath.endswith('.json'):
                    await f.write(json.dumps(self.data_store, indent=4))
                elif filepath.endswith('.yaml') or filepath.endswith('.yml'):
                    content = yaml.dump(self.data_store)
                    await f.write(content)
                else:
                    raise ValueError("Unsupported file type. Please use JSON or YAML.")
            return True
        except Exception as e:
            print(f"An error occurred while saving to file: {e}")
            return False

