# Arsenix Documentation

Welcome to the official documentation for Arsenix, a high-performance Python library for building scalable recommendation engines.

## Quick Start

Get started in minutes with our pre-built FYP strategies.

### Trending Feed

```python
from arsenix import ArsenixServer, TrendingFYP

server = ArsenixServer()
await server.load_from_file('data.json')

trending_feed = await TrendingFYP(server)
print(trending_feed)
```

### Personalized Feed

```python
from arsenix import ArsenixServer, PersonalizedFYP

server = ArsenixServer()
await server.load_from_file('data.json')

personalized_feed = await PersonalizedFYP(server, user_id='user_123')
print(personalized_feed)
```

## Custom Algorithms with FYPBuilder

For more advanced use cases, the `FYPBuilder` provides a flexible, chainable interface for creating custom recommendation algorithms.

```python
from arsenix import FYPBuilder

items = await server.get('items', {})

builder = FYPBuilder(items)
recommendations = await builder.match_tags(['tech', 'ai'], weight=2.0) \
                               .boost_recency(1.5) \
                               .limit(10) \
                               .run()

print(recommendations)
```

## Key Features

- **Rule + Score Mixing Engine**: A declarative interface for building custom algorithms.
- **Pre-Built Strategies**: Ready-to-use functions for common recommendation scenarios.
- **Asynchronous by Design**: Built on `asyncio` for high performance and scalability.
- **Pluggable Caching**: Support for local, disk, and Redis caching.


## Table of Contents

- [Introduction](./introduction.md)
- [Getting Started](./getting-started.md)
- [API Reference](./api-reference.md)
- [Examples](./examples.md)

## Quick Links

- [GitHub Repository](https://github.com/mebaadwaheed/arsenix)
- [Report an Issue](https://github.com/mebaadwaheed/arsenix/issues)
