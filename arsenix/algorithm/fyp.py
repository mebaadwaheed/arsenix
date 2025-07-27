class FYPBuilder:
    """A declarative builder for creating and executing recommendation algorithms."""
    def __init__(self, items):
        """Initializes the FYPBuilder with a set of items to process.

        Args:
            items (dict): A dictionary of items to be processed by the algorithm.
        """
        self.items = list(items.values())
        self._steps = []

    def match_tags(self, tags):
        """Adds a step to the algorithm to filter items by a set of tags.

        Args:
            tags (list): A list of tags to match against the items.

        Returns:
            FYPBuilder: The builder instance for chaining methods.
        """
        self._steps.append(('match_tags', {'tags': tags}))
        return self

    def sort_by(self, key, reverse=True):
        """Adds a step to the algorithm to sort items by a specific key.

        Args:
            key (str): The dictionary key to sort the items by.
            reverse (bool, optional): Whether to sort in descending order. Defaults to True.

        Returns:
            FYPBuilder: The builder instance for chaining methods.
        """
        self._steps.append(('sort_by', {'key': key, 'reverse': reverse}))
        return self

    def limit(self, count):
        """Adds a step to the algorithm to limit the number of returned items.

        Args:
            count (int): The maximum number of items to return.

        Returns:
            FYPBuilder: The builder instance for chaining methods.
        """
        self._steps.append(('limit', {'count': count}))
        return self

    async def run(self):
        """Asynchronously executes the configured algorithm steps on the items.

        The steps are executed in the order they were added.

        Returns:
            list: A list of processed and sorted items.
        """
        processed_items = self.items

        for step, params in self._steps:
            if step == 'match_tags':
                tags_to_match = set(params.get('tags', []))
                processed_items = [item for item in processed_items if tags_to_match.intersection(item.get('tags', []))]

            elif step == 'sort_by':
                processed_items.sort(key=lambda x: x.get(params['key'], 0), reverse=params['reverse'])

            elif step == 'limit':
                processed_items = processed_items[:params['count']]

        return processed_items
