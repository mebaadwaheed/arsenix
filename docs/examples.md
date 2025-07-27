# Examples

This document provides a set of practical examples that demonstrate how to use the `FYPBuilder` and the pre-built FYP strategies to create sophisticated recommendation feeds.

## Example 1: Building a Custom Feed for a Social Media App

In this example, we'll build a custom feed for a social media app that prioritizes recent content, boosts posts with high engagement, and demotes posts with negative feedback.

```python
import asyncio
from arsenix import ArsenixServer, FYPBuilder

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
from arsenix import ArsenixServer, TrendingFYP

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
from arsenix import ArsenixServer, PersonalizedFYP

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