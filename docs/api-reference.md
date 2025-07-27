# API Reference

This document provides a detailed reference for the core components of the Arsenix library, including the `FYPBuilder` and the pre-built FYP strategies.

## FYPBuilder

The `FYPBuilder` is a declarative interface for creating custom recommendation algorithms. You can chain together various methods to build a sophisticated scoring and ranking engine.

### `__init__(self, items)`
Initializes the builder with a set of items to process.

- **items** (`dict`): A dictionary of items to be processed.

### `match_tags(self, tags, weight=1.0)`
Adds a rule to boost items that match a set of tags. The score is increased by the `weight` multiplied by the number of matching tags.

- **tags** (`list`): A list of tags to match.
- **weight** (`float`, optional): The weight to apply for each matching tag. Defaults to `1.0`.

### `boost_by_key(self, key, factor)`
Adds a rule to boost items based on a numerical key. The score is multiplied by `(1 + log(1 + value) * factor)`.

- **key** (`str`): The dictionary key to use for boosting.
- **factor** (`float`): The factor to apply to the boost.

### `demote_by_key(self, key, factor)`
Adds a rule to demote items based on a numerical key. The score is divided by `(1 + log(1 + value) * factor)`.

- **key** (`str`): The dictionary key to use for demoting.
- **factor** (`float`): The factor to apply to the demotion.

### `boost_recency(self, factor, time_key='timestamp')`
Adds a rule to boost items based on their recency. The score is multiplied by a recency score calculated from the item's age.

- **factor** (`float`): The factor to apply to the recency score.
- **time_key** (`str`, optional): The key containing the item's timestamp. Defaults to `'timestamp'`.

### `sort_by(self, key, reverse=True)`
Adds a final sorting step that overrides the default score-based sort.

- **key** (`str`): The dictionary key to sort by.
- **reverse** (`bool`, optional): Whether to sort in descending order. Defaults to `True`.

### `limit(self, count)`
Limits the number of items returned.

- **count** (`int`): The maximum number of items to return.

### `run(self)`
Executes the configured algorithm and returns the processed items.

## Pre-Built FYP Strategies

Arsenix provides pre-built functions for common recommendation scenarios.

### `TrendingFYP(server)`
Generates a trending feed by boosting items with high engagement and recent activity.

- **server** (`ArsenixServer`): The Arsenix server instance.

### `PersonalizedFYP(server, user_id)`
Generates a personalized feed for a user based on their interests.

- **server** (`ArsenixServer`): The Arsenix server instance.
- **user_id** (`str`): The ID of the user.

