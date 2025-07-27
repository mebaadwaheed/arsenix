import pytest
import time 
from arsenix import ArsenixServer
from arsenix.algorithm import FYPBuilder
from arsenix.presets import TrendingFYP, PersonalizedFYP

@pytest.fixture
def server():
    """Provides a test instance of the ArsenixServer with sample data."""
    # Sample data for items and users
    items = {
        'item1': {'id': 'item1', 'tags': ['tech', 'ai'], 'likes': 100, 'views': 1000, 'timestamp': time.time() - 86400, 'creator_id': 'creator1', 'creator_followers': 1000},
        'item2': {'id': 'item2', 'tags': ['health', 'fitness'], 'likes': 200, 'views': 500, 'timestamp': time.time() - 172800, 'creator_id': 'creator2', 'creator_followers': 5000},
        'item3': {'id': 'item3', 'tags': ['tech', 'python'], 'likes': 50, 'views': 2000, 'timestamp': time.time(), 'creator_id': 'creator1', 'creator_followers': 1000}
    }
    users = {
        'user1': {'id': 'user1', 'interests': ['tech', 'python'], 'following': ['creator1']}
    }
    data_store = {'items': items, 'users': users}
    return ArsenixServer(data_store)

@pytest.mark.asyncio
async def test_fyp_builder_scoring(server):
    """Tests the core scoring and rule-mixing engine of the FYPBuilder."""
    items = await server.get('items')
    builder = FYPBuilder(items)

    # Build a custom algorithm
    result = await builder.match_tags(['tech'], weight=2.0).boost_recency(1.5).boost_by_key('likes', 1.2).limit(2).run()

    # Ensure the results are sorted by score
    assert len(result) == 2
    assert result[0]['_score'] > result[1]['_score']
    assert result[0]['id'] == 'item3' # With logarithmic scoring, recency and tags have a stronger influence

@pytest.mark.asyncio
async def test_trending_fyp(server):
    """Tests the TrendingFYP pre-built strategy."""
    result = await TrendingFYP(server)

    # Ensure the feed is generated and sorted
    assert len(result) > 0
    assert result[0]['_score'] > result[1]['_score']
    # item3 is newest and has high views, should be a top contender
    # item2 has most likes
    # Depending on weighting, either could be first. Just check for order.

@pytest.mark.asyncio
async def test_personalized_fyp(server):
    """Tests the PersonalizedFYP pre-built strategy."""
    result = await PersonalizedFYP(server, user_id='user1')

    # The user is interested in 'tech' and 'python', so item3 should be first
    assert len(result) > 0
    assert result[0]['id'] == 'item3' # The user is interested in 'tech' and 'python', so item3 should be first

@pytest.mark.asyncio
async def test_personalized_fyp_user_not_found(server):
    """Tests the PersonalizedFYP strategy for a user that does not exist."""
    result = await PersonalizedFYP(server, user_id='non_existent_user')
    assert result == []
