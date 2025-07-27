# Examples

This section provides practical examples demonstrating how to use the core features of Arsenix in a real-world scenario.

## Comprehensive Example: Recommendation Engine

This example showcases how to use Arsenix to build a simple recommendation engine that suggests content based on scores, caches the results, and learns user patterns.

```python
import asyncio
from arsenix import ArsenixServer
from arsenix.algorithm import FYPBuilder

async def main():
    # 1. Initialize ArsenixServer
    server = ArsenixServer()

    # 2. Add sample data using ARSetter
    await server.set("video1", {"score": 90, "tags": ["funny", "cat"]})
    await server.set("video2", {"score": 75, "tags": ["tech", "ai"]})
    await server.set("video3", {"score": 95, "tags": ["funny", "dog"]})

    print(f"Initial data store: {server.data_store}")

    # 3. Get recommendations using FYPBuilder
    recommended = await FYPBuilder(list(server.data_store.values()))
    print(f"\nRecommended content: {recommended}")

    # 4. Cache the results using LocalCache
    await server.cache.put("user123_recommendations", recommended)
    cached_result = await server.cache.get("user123_recommendations")
    print(f"\nCached recommendations: {cached_result}")

    # 5. Learn user interests with the Pattern system
    await server.pattern.learn("user123", ["funny", "tech", "ai"])
    user_pattern = await server.pattern.get_pattern("user123")
    print(f"\nLearned pattern for user123: {user_pattern}")

if __name__ == "__main__":
    asyncio.run(main())
```

### How It Works

1.  **Initialization**: An `ArsenixServer` instance is created.
2.  **Data Seeding**: Sample video data with scores and tags is added to the data store.
3.  **Recommendation**: The `FYPBuilder` function sorts the videos by score to create a ranked list.
4.  **Caching**: The recommendation results are stored in the `LocalCache` for fast retrieval.
5.  **Pattern Learning**: The system learns that `user123` is interested in `funny`, `tech`, and `ai` tags.
