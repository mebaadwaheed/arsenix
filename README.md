# Arsenix: The Async-First Personalization Toolkit

[![PyPI version](https://badge.fury.io/py/arsenixpy.svg)](https://pypi.org/project/arsenix/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Arsenix is a modern, lightweight, and async-first Python library designed for building sophisticated personalization and recommendation systems with ease. It provides a flexible and modular toolkit for tracking user behavior, managing data, and generating real-time recommendations.

## Why Arsenix?

In a world of monolithic and complex recommendation frameworks, Arsenix stands out by being:

-   **Async-First by Design**: Built from the ground up with `asyncio`, Arsenix is perfect for high-performance, I/O-bound applications, ensuring your recommendation engine never blocks your main thread.
-   **Pluggable Caching**: Swap caching backends on the fly. Start with a simple in-memory cache, then scale up to `DiskCache` or `Redis` without changing your application logic.
-   **Declarative Algorithm Builder**: Construct complex recommendation pipelines with a simple, chainable API. The `FYPBuilder` lets you define how to filter, sort, and rank items declaratively, making your code more readable and maintainable.
-   **Lightweight and Zero-Dependency (Core)**: The core library is dependency-free, keeping your environment clean. Optional features like advanced caching can be installed as needed, so you only pay for what you use.

## Core Features

-   **Real-time Pattern Learning**: Automatically learn user interest patterns from their interactions.
-   **Multi-User Recommendations**: Generate personalized "For You Page" (FYP) style recommendations for each user.
-   **Flexible Data Store**: A simple dictionary-based data store with asynchronous getters and setters.
-   **Built-in Persistence**: Easily save and load your data store to and from JSON or YAML files.
-   **Pluggable Cache Engines**:
    -   `LocalCache`: In-memory dictionary cache (default).
    -   `DiskCache`: File-based cache for persistence between sessions.
    -   `RedisCache`: High-performance caching using a Redis server.

## Getting Started

### Installation

Install the core library via pip:

```bash
pip install arsenix
```

To include support for `DiskCache` and `RedisCache`, install the optional extras:

```bash
pip install arsenix[diskcache,redis]
```

### Quick Example

Here's how easy it is to get personalized recommendations:

```python
import asyncio
from arsenix.server import ArsenixServer

async def main():
    # 1. Initialize the server with some items
    data_store = {
        'item1': {'id': 'item1', 'tags': ['tech', 'python']},
        'item2': {'id': 'item2', 'tags': ['funny', 'cats']},
        'item3': {'id': 'item3', 'tags': ['tech', 'ai']},
    }
    server = ArsenixServer(data_store)

    # 2. Learn a user's interests
    user_id = 'user_123'
    await server.pattern.learn(user_id, ['tech', 'python'])

    # 3. Get recommendations for that user
    recommendations = await server.get_recommendations(user_id)
    print(recommendations)
    # Output: [{'id': 'item1', 'tags': ['tech', 'python']}]

if __name__ == "__main__":
    asyncio.run(main())
```

## Documentation

For a deep dive into the API, advanced usage, and more examples, check out our full documentation in the [Documentation](./docs/README.md).

## License

Arsenix is licensed under the MIT License. See the `LICENSE` file for more details.
