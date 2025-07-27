# Getting Started with Arsenix

This guide will walk you through the process of installing Arsenix and running your first asynchronous application.

## Installation

Arsenix is available on PyPI and can be installed using pip. To install the library, run the following command in your terminal:

```bash
pip install arsenix
```

This will install Arsenix along with its required dependencies, `PyYAML` and `aiofiles`.

## Your First Arsenix Application

Let's create a simple example to see Arsenix in action. The following script initializes the `ArsenixServer`, adds a piece of data, and retrieves it.

Create a file named `main.py` and add the following code:

```python
import asyncio
from arsenix import ArsenixServer

async def main():
    # Initialize the server
    server = ArsenixServer()

    # Set a key-value pair
    await server.set("message", "Hello, Arsenix!")

    # Get the value
    message = await server.get("message")
    print(message)

if __name__ == "__main__":
    asyncio.run(main())
```

### Running the Example

To run the script, execute the following command in your terminal:

```bash
python main.py
```

You should see the following output:

```
Hello, Arsenix!
```

Congratulations! You've successfully built and run your first application with Arsenix. Now you're ready to explore its more advanced features.
