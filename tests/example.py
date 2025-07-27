import asyncio
from arsenix import ArsenixServer
from arsenix.algorithm import FYPBuilder

async def main():
    # 1. Initialize ArsenixServer
    server = ArsenixServer()

    # 2. Use ARSetter to add sample data
    await server.set("video1", {"score": 90, "tags": ["funny", "cat"]})
    await server.set("video2", {"score": 75, "tags": ["tech", "ai"]})
    await server.set("video3", {"score": 95, "tags": ["funny", "dog"]})

    print(f"Initial data store: {server.data_store}")

    # 3. Use FYPBuilder to get recommendations
    recommended = await FYPBuilder(list(server.data_store.values()))
    print(f"\nRecommended content: {recommended}")

    # 4. Use LocalCache to store the results
    await server.cache.put("user123_recommendations", recommended)
    cached_result = await server.cache.get("user123_recommendations")
    print(f"\nCached recommendations: {cached_result}")

    # 5. Use the Pattern system to learn user interests
    await server.pattern.learn("user123", ["funny", "tech", "ai"])
    user_pattern = await server.pattern.get_pattern("user123")
    print(f"\nLearned pattern for user123: {user_pattern}")

if __name__ == "__main__":
    asyncio.run(main())
