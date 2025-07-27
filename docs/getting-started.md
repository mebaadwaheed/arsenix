# Getting Started with Arsenix

Welcome to Arsenix, a powerful and flexible library for building recommendation engines. This guide will walk you through the basics of setting up the server, using the `FYPBuilder` to create custom algorithms, and leveraging pre-built strategies for common use cases.

## Installation

To get started, install Arsenix using pip:

```bash
pip install arsenix
```

## Initializing the Server

The `ArsenixServer` is the central component of the library. It manages your data and provides the interface for all other features.

```python
from arsenix import ArsenixServer

# Initialize the server
server = ArsenixServer()

# Load data from a file (optional)
await server.load_from_file('your_data.json')
```

## Building a Custom Feed with FYPBuilder

The `FYPBuilder` provides a declarative, chainable interface for building sophisticated recommendation algorithms using a rule-and-score engine.

```python
from arsenix.algorithm import FYPBuilder

# Get items from the server
items = await server.get('items', {})

# Build a custom algorithm
builder = FYPBuilder(items)
recommendations = await builder.match_tags(['tech', 'ai'], weight=2.0) \
                               .boost_recency(1.5) \
                               .boost_by_key('likes', 0.1) \
                               .limit(10) \
                               .run()

print(recommendations)
```

## Using Pre-Built FYP Strategies

Arsenix also provides pre-built strategies for common use cases, allowing you to get up and running quickly.

### Trending Feed

Generate a trending feed based on engagement and recency.

```python
from arsenix.presets import TrendingFYP

trending_feed = await TrendingFYP(server)
print(trending_feed)
```

### Personalized Feed

Generate a personalized feed for a specific user based on their interests.

```python
from arsenix.presets import PersonalizedFYP

personalized_feed = await PersonalizedFYP(server, user_id='user_123')
print(personalized_feed)
```