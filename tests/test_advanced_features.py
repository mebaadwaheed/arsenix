import pytest
import asyncio
import os
from arsenix import ArsenixServer

try:
    import redis.asyncio as redis
    from redis.exceptions import ConnectionError as RedisConnectionError
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False

# Sample data for testing
SAMPLE_DATA = {
    'item1': {'id': 'item1', 'tags': ['tech', 'ai'], 'popularity': 80},
    'item2': {'id': 'item2', 'tags': ['funny', 'cat'], 'popularity': 90},
    'item3': {'id': 'item3', 'tags': ['tech', 'python'], 'popularity': 85},
    'item4': {'id': 'item4', 'tags': ['funny', 'dog'], 'popularity': 95},
}

@pytest.fixture
def server():
    """Provides a clean ArsenixServer instance for each test."""
    return ArsenixServer(data_store=SAMPLE_DATA.copy())

@pytest.mark.asyncio
async def test_pluggable_disk_cache(server):
    """Tests switching to and using the DiskCache."""
    cache_dir = './test_cache'
    server.use_cache('diskcache', directory=cache_dir)
    
    await server.cache.put('test_key', 'test_value')
    retrieved_value = await server.cache.get('test_key')
    
    assert retrieved_value == 'test_value'
    
    # Cleanup
    server.cache._cache.close()
    if os.path.exists(cache_dir):
        import shutil
        shutil.rmtree(cache_dir)

@pytest.mark.asyncio
async def test_persistence_sync(server):
    """Tests saving and loading the data store using the sync method."""
    filepath = 'test_store.json'
    
    # Save the current data store
    save_success = await server.sync('save', filepath=filepath)
    assert save_success
    assert os.path.exists(filepath)
    
    # Create a new server and load the data
    new_server = ArsenixServer()
    load_success = await new_server.sync('load', filepath=filepath)
    assert load_success
    
    # Verify the data was loaded correctly
    loaded_item = await new_server.get('item1')
    assert loaded_item == SAMPLE_DATA['item1']
    
    # Cleanup
    os.remove(filepath)

@pytest.mark.asyncio
async def test_auto_pattern_learner(server):
    """Tests the auto_learn method for tracking user behavior."""
    user_id = 'user_test_123'
    tags = ['tech', 'python']
    
    await server.pattern.auto_learn(user_id, tags)
    
    learned_pattern = await server.pattern.get_pattern(user_id)
    assert learned_pattern['tech'] == 1
    assert learned_pattern['python'] == 1

@pytest.mark.asyncio
async def test_multi_user_recommendations(server):
    """Tests the get_recommendations method for personalized content."""
    user_id = 'reco_user_456'
    
    # First, learn some user patterns
    await server.pattern.learn(user_id, ['funny', 'dog'])
    
    # Get recommendations based on the learned pattern
    recommendations = await server.get_recommendations(user_id, top_n=2, limit=1)
    
    assert len(recommendations) == 1
    # The top recommendation should be item4, as it matches the 'funny' and 'dog' tags and has the highest popularity
    assert recommendations[0]['id'] == 'item4'

@pytest.mark.skipif(not REDIS_AVAILABLE, reason="redis is not installed or not available")
@pytest.mark.asyncio
async def test_pluggable_redis_cache(server):
    """Tests switching to and using the RedisCache."""
    try:
        # Check for a running Redis instance
        r = redis.Redis()
        await r.ping()
    except (RedisConnectionError, AttributeError):
        pytest.skip("Redis server not available on localhost:6379")

    server.use_cache('redis')
    
    await server.cache.put('redis_test_key', {'a': 1})
    retrieved_value = await server.cache.get('redis_test_key')
    
    assert retrieved_value == {'a': 1}
    
    # Cleanup
    await server.cache.clear()
