import json
import yaml
import aiofiles

class ARSetter:
    def __init__(self, data_store):
        if not isinstance(data_store, dict):
            raise TypeError("data_store must be a dictionary.")
        self.data_store = data_store

    async def set(self, key, value):
        """Sets or updates a key-value pair in the data store."""
        self.data_store[key] = value
        return True

    async def update(self, key, new_value):
        """Updates an existing entry. Returns False if the key doesn't exist."""
        if key in self.data_store:
            if isinstance(self.data_store[key], dict) and isinstance(new_value, dict):
                self.data_store[key].update(new_value)
            else:
                self.data_store[key] = new_value
            return True
        return False

    async def delete(self, key):
        """Deletes an entry by key. Returns False if the key doesn't exist."""
        if key in self.data_store:
            del self.data_store[key]
            return True
        return False

    async def bulk_set(self, data):
        """Adds multiple entries to the data store from a dictionary."""
        if not isinstance(data, dict):
            raise TypeError("Input data must be a dictionary.")
        self.data_store.update(data)
        return True

    async def load_from_file(self, filepath):
        """Loads data from a JSON or YAML file and adds it to the data store."""
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

