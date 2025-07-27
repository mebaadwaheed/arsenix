async def FYPBuilder(items):
    """Sorts a list of items based on their score in descending order."""
    if not isinstance(items, list):
        raise TypeError("Input must be a list of items.")

    # Filter out items that are not dictionaries or do not have a 'score' key
    scored_items = [item for item in items if isinstance(item, dict) and 'score' in item]

    # Sort the items by score in descending order
    return sorted(scored_items, key=lambda x: x['score'], reverse=True)
