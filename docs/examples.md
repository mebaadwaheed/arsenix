# Examples

This document provides a set of practical examples that demonstrate how to use the `FYPBuilder` and the pre-built FYP strategies to create sophisticated recommendation feeds.

## Example 1: Building a Custom Feed for a Social Media App

In this example, we'll build a custom feed for a social media app that prioritizes recent content, boosts posts with high engagement, and demotes posts with negative feedback.

```python
import asyncio
from arsenix import ArsenixServer
from arsenix.algorithm import FYPBuilder

async def main():
    # Initialize the server and load data
    server = ArsenixServer()
    await server.load_from_file('social_media_data.json')

    # Get items from the server
    items = await server.get('posts', {})

    # Build the custom feed
    builder = FYPBuilder(items)
    recommendations = await builder.boost_recency(1.5) \
                                   .boost_by_key('likes', 0.2) \
                                   .boost_by_key('shares', 0.3) \
                                   .demote_by_key('reports', 0.5) \
                                   .limit(20) \
                                   .run()

    print("Custom Social Media Feed:", recommendations)

if __name__ == "__main__":
    asyncio.run(main())
```

## Example 2: Using the TrendingFYP Strategy

This example demonstrates how to use the `TrendingFYP` pre-built strategy to quickly generate a trending feed.

```python
import asyncio
from arsenix import ArsenixServer
from arsenix.presets import TrendingFYP

async def main():
    # Initialize the server and load data
    server = ArsenixServer()
    await server.load_from_file('trending_data.json')

    # Generate the trending feed
    trending_feed = await TrendingFYP(server)

    print("Trending Feed:", trending_feed)

if __name__ == "__main__":
    asyncio.run(main())
```

## Example 3: Using the PersonalizedFYP Strategy

This example shows how to use the `PersonalizedFYP` pre-built strategy to generate a feed tailored to a specific user's interests.

```python
import asyncio
from arsenix import ArsenixServer
from arsenix.presets import PersonalizedFYP

async def main():
    # Initialize the server and load data
    server = ArsenixServer()
    await server.load_from_file('user_data.json')

    # Generate a personalized feed for user 'user_456'
    personalized_feed = await PersonalizedFYP(server, user_id='user_456')

    print("Personalized Feed for user_456:", personalized_feed)

if __name__ == "__main__":
    asyncio.run(main())
```

## Example 4: Using Pluggable Caching

This example demonstrates how to switch the caching engine to `DiskCache` for persistent caching.

```python
import asyncio
from arsenix import ArsenixServer

async def main():
    # Initialize the server
    server = ArsenixServer()

    # Switch to DiskCache
    server.use_cache('diskcache', directory='my_app_cache')

    # Use the cache
    await server.cache.put('user_session', {'id': 'user1', 'status': 'active'})
    session = await server.cache.get('user_session')
    print("Cached Session:", session)

if __name__ == "__main__":
    asyncio.run(main())
```

## Example 5: Learning User Patterns

This example shows how to learn a user's interests from their interactions and then retrieve the learned pattern.

```python
import asyncio
from arsenix import ArsenixServer

async def main():
    # Initialize the server
    server = ArsenixServer()

    # Learn a user's interests
    await server.pattern.learn('user1', ['tech', 'python', 'ai'])
    await server.pattern.learn('user1', ['tech', 'async'])

    # Get the user's learned pattern
    user_pattern = await server.pattern.get_pattern('user1')
    print("Learned Pattern for user1:", user_pattern)

if __name__ == "__main__":
    asyncio.run(main())