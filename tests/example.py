import asyncio
import time
from arsenix import ArsenixServer
from arsenix.algorithm import FYPBuilder
from arsenix.presets import TrendingFYP, PersonalizedFYP

# Sample data for the recommendation engine
SAMPLE_DATA = {
    'items': {
        'item1': {'id': 'item1', 'tags': ['tech', 'python', 'async'], 'views': 150, 'likes': 90, 'timestamp': time.time() - 3600, 'creator_followers': 1000},
        'item2': {'id': 'item2', 'tags': ['funny', 'cats', 'videos'], 'views': 500, 'likes': 450, 'timestamp': time.time() - 7200, 'creator_followers': 5000},
        'item3': {'id': 'item3', 'tags': ['tech', 'ai', 'deep-learning'], 'views': 300, 'likes': 250, 'timestamp': time.time() - 1800, 'creator_followers': 10000},
        'item4': {'id': 'item4', 'tags': ['python', 'tutorial'], 'views': 80, 'likes': 75, 'timestamp': time.time() - 10800, 'creator_followers': 2500},
    },
    'users': {
        'user1': {'id': 'user1', 'interests': ['tech', 'python']},
        'user2': {'id': 'user2', 'interests': ['cats', 'videos']},
    }
}

async def main():
    """
    An example script to demonstrate the new features of Arsenix.
    """
    print("--- Initializing Arsenix Server and loading data ---")
    server = ArsenixServer(data_store=SAMPLE_DATA)
    
    print("\n--- 1. Generating a Trending Feed ---")
    trending_feed = await TrendingFYP(server)
    print("Trending Feed Results:", [item['id'] for item in trending_feed])

    print("\n--- 2. Generating a Personalized Feed for user1 ---")
    personalized_feed = await PersonalizedFYP(server, user_id='user1')
    print("Personalized Feed Results:", [item['id'] for item in personalized_feed])

    print("\n--- 3. Building a Custom Feed with FYPBuilder ---")
    items = await server.get('items', {})
    custom_feed = await FYPBuilder(items) \
        .match_tags(['python'], weight=1.5) \
        .boost_by_key('creator_followers', factor=0.1) \
        .boost_recency(factor=1.2) \
        .limit(2) \
        .run()
    print("Custom Feed Results:", [item['id'] for item in custom_feed])

if __name__ == "__main__":
    asyncio.run(main())