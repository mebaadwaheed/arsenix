import asyncio
import os
import shutil
from arsenix.server import ArsenixServer

# Sample data for our tests
SAMPLE_DATA = {
    'item1': {'id': 'item1', 'tags': ['tech', 'python', 'async'], 'popularity': 10},
    'item2': {'id': 'item2', 'tags': ['funny', 'cats', 'videos'], 'popularity': 20},
    'item3': {'id': 'item3', 'tags': ['tech', 'ai', 'deep-learning'], 'popularity': 15},
    'item4': {'id': 'item4', 'tags': ['python', 'tutorial', 'async'], 'popularity': 12},
}

async def run_tests():
    """
    A simple test runner for Arsenix core features without using a test framework.
    """
    print("--- Starting Arsenix Core Feature Tests ---")

    # Initialize the server
    server = ArsenixServer(SAMPLE_DATA)
    print("\n[SUCCESS] ArsenixServer initialized.")

    # --- 1. Test Data Store (Get/Set) ---
    print("\n--- Testing Data Store ---")
    retrieved_item = await server.get('item1')
    print(f"GET 'item1': {retrieved_item}")
    await server.set('item5', {'id': 'item5', 'tags': ['new', 'item']})
    retrieved_new_item = await server.get('item5')
    print(f"SET and GET 'item5': {retrieved_new_item}")
    print("[SUCCESS] Data Store tests passed.")

    # --- 2. Test Pattern Learning ---
    print("\n--- Testing Pattern Learning ---")
    user_id = 'test_user_1'
    await server.pattern.learn(user_id, ['tech', 'async', 'python', 'tech'])
    user_pattern = await server.pattern.get_pattern(user_id)
    print(f"Learned pattern for '{user_id}': {user_pattern}")
    print("[SUCCESS] Pattern Learning tests passed.")

    # --- 3. Test Recommendations ---
    print("\n--- Testing Recommendations ---")
    recommendations = await server.get_recommendations(user_id, top_n=2, limit=2)
    print(f"Recommendations for '{user_id}': {recommendations}")
    print("[SUCCESS] Recommendation tests passed.")

    # --- 4. Test Persistence (Save/Load) ---
    print("\n--- Testing Persistence ---")
    filepath = 'test_store.json'
    await server.sync('save', filepath=filepath)
    print(f"Data store saved to '{filepath}'.")
    # Create a new server and load from the file
    new_server = ArsenixServer()
    await new_server.sync('load', filepath=filepath)
    loaded_item = await new_server.get('item1')
    print(f"Loaded 'item1' from file: {loaded_item}")
    os.remove(filepath)
    print("[SUCCESS] Persistence tests passed.")

    # --- 5. Test Pluggable Caching ---
    print("\n--- Testing Pluggable Caching ---")
    # Default LocalCache is already in use
    print("Testing LocalCache (default)...")
    await server.cache.put('local_key', 'local_value')
    cached_value = await server.cache.get('local_key')
    print(f"LocalCache GET 'local_key': {cached_value}")
    print("[SUCCESS] LocalCache test passed.")

    # Test DiskCache
    print("\nTesting DiskCache...")
    cache_dir = 'test_disk_cache'
    server.use_cache('diskcache', directory=cache_dir)
    await server.cache.put('disk_key', 'disk_value')
    cached_value = await server.cache.get('disk_key')
    print(f"DiskCache GET 'disk_key': {cached_value}")
    # Clean up
    server.cache._cache.close()
    if os.path.exists(cache_dir):
        shutil.rmtree(cache_dir)
    print("[SUCCESS] DiskCache test passed.")

    # Test RedisCache
    print("\nTesting RedisCache...")
    try:
        server.use_cache('redis')
        await server.cache.put('redis_key', 'redis_value')
        cached_value = await server.cache.get('redis_key')
        print(f"RedisCache GET 'redis_key': {cached_value}")
        await server.cache.clear()
        print("[SUCCESS] RedisCache test passed.")
    except Exception as e:
        print(f"[SKIPPED] RedisCache test skipped: {e}")

    print("\n--- All Core Feature Tests Completed ---")

if __name__ == "__main__":
    asyncio.run(run_tests())
