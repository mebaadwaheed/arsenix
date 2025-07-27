import os
import shutil
import pytest
from arsenix.server import ArsenixServer

@pytest.mark.asyncio
async def test_pattern_learning():
    """Tests the pattern learning and retrieval functionality."""
    server = ArsenixServer()
    user_id = 'test_user'
    interests = ['gaming', 'esports', 'streaming']
    
    await server.pattern.learn(user_id, interests)
    await server.pattern.learn(user_id, ['gaming', 'reviews'])
    
    learned_pattern = await server.pattern.get_pattern(user_id)
    
    assert learned_pattern['gaming'] == 2
    assert learned_pattern['esports'] == 1
    assert learned_pattern['streaming'] == 1
    assert learned_pattern['reviews'] == 1

@pytest.mark.asyncio
async def test_disk_cache():
    """Tests the DiskCache functionality for persistent caching."""
    cache_dir = 'test_cache'
    server = ArsenixServer()
    server.use_cache('diskcache', directory=cache_dir)
    
    try:
        key = 'test_key'
        value = {'data': 'some_cached_value'}
        
        await server.cache.put(key, value)
        cached_value = await server.cache.get(key)
        
        assert cached_value == value
        
        await server.cache.delete(key)
        deleted_value = await server.cache.get(key)
        
        assert deleted_value is None
    finally:
        # Close the cache to release the file lock before cleaning up
        server.cache._cache.close()
        # Clean up the cache directory
        if os.path.exists(cache_dir):
            shutil.rmtree(cache_dir)
