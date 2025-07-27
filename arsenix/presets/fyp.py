from ..algorithm.fyp import FYPBuilder

async def TrendingFYP(server):
    """Runs a pre-built algorithm to generate a trending feed.

    This strategy boosts items with high engagement (likes, views) and recent activity
    to determine what's currently popular.

    Args:
        server (ArsenixServer): The Arsenix server instance.

    Returns:
        list: A list of trending items, sorted by popularity.
    """
    items = await server.get('items', {})
    builder = FYPBuilder(items)
    
    # Boost by likes and views, and also recency
    result = await builder.boost_by_key('likes', 1.5).boost_by_key('views', 1.2).boost_recency(1.5).limit(20).run()
    return result

async def PersonalizedFYP(server, user_id):
    """Runs a pre-built algorithm to generate a personalized feed for a specific user.

    This strategy tailors the feed based on the user's interests and past interactions,
    such as boosting content from creators they follow.

    Args:
        server (ArsenixServer): The Arsenix server instance.
        user_id (str): The ID of the user for whom the feed is being generated.

    Returns:
        list: A list of personalized items, sorted by relevance to the user.
    """
    items = await server.get('items', {})
    users = await server.get('users', {})
    user = users.get(user_id)

    if not user:
        return []

    builder = FYPBuilder(items)

    # Match user's interests and boost content from creators with more followers
    result = await builder.match_tags(user.get('interests', []), weight=2.0).boost_by_key('creator_followers', 0.1).limit(20).run()
    return result
