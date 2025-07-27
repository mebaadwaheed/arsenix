# API Reference

This document provides a detailed overview of the public API for the Arsenix library. All core components are designed to be asynchronous.

## `ArsenixServer`

The `ArsenixServer` is the main entry point for interacting with the library.

- `__init__(self, data_store=None)`: Initializes the server. If `data_store` is not provided, an empty dictionary is created.
- `async get(self, key, default=None)`: Retrieves a value from the data store.
- `async set(self, key, value)`: Sets a key-value pair in the data store.
- `async load_from_file(self, filepath)`: Loads data from a JSON or YAML file into the data store.
- `use_cache(self, provider, **kwargs)`: Switches the caching engine. 
- `async sync(self, action, filepath='arsenix_store.json')`: Saves or loads the data store to/from a file.
- `async get_recommendations(self, user_id, top_n=3, limit=10)`: Generates personalized recommendations for a user.

## `ARGetter`

- `async get(self, key, default=None)`: Retrieves a value by key from the associated data store.

## `ARSetter`

- `async set(self, key, value)`: Sets or updates a key-value pair.
- `async update(self, key, new_value)`: Updates an existing entry.
- `async delete(self, key)`: Deletes an entry by key.
- `async bulk_set(self, data)`: Adds multiple entries from a dictionary.
- `async load_from_file(self, filepath)`: Loads data from a JSON or YAML file.

## `LocalCache`

- `async get(self, key, default=None)`: Retrieves an item from the cache.
- `async put(self, key, value)`: Adds an item to the cache.
- `async delete(self, key)`: Removes an item from the cache.
- `async clear(self)`: Clears the entire cache.

## `FYPBuilder`

- `async FYPBuilder(items)`: Sorts a list of dictionary items based on their `score` in descending order.

## `Pattern`

- `async learn(self, user_id, interests)`: Learns and updates the interest pattern for a user.
- `async get_pattern(self, user_id)`: Retrieves the learned interest pattern for a user.
- `async auto_learn(self, user_id, tags)`: An alias for the `learn` method to track user behavior automatically.
- `async get_all_patterns(self)`: Returns all learned user patterns.
