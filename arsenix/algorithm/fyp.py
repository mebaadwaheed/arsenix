import time
import math

class FYPBuilder:
    """A declarative builder for creating and executing recommendation algorithms."""
    def __init__(self, items):
        """Initializes the FYPBuilder with a set of items to process.

        Args:
            items (dict): A dictionary of items to be processed by the algorithm.
        """
        self.items = list(items.values())
        self._steps = []
        self._scores = {item['id']: 1.0 for item in self.items}
        self._sort_params = None

    def match_tags(self, tags, weight=1.0):
        """Adds a rule to boost items that match a set of tags.

        Args:
            tags (list): A list of tags to match against.
            weight (float, optional): The weight to apply to matching items. Defaults to 1.0.

        Returns:
            FYPBuilder: The builder instance for chaining methods.
        """
        self._steps.append(('match_tags', {'tags': tags, 'weight': weight}))
        return self

    def boost_by_key(self, key, factor):
        """Adds a rule to boost items based on a numerical key.

        Args:
            key (str): The dictionary key to use for boosting.
            factor (float): The factor to multiply the score by.

        Returns:
            FYPBuilder: The builder instance for chaining methods.
        """
        self._steps.append(('boost_by_key', {'key': key, 'factor': factor}))
        return self

    def demote_by_key(self, key, factor):
        """Adds a rule to demote items based on a numerical key.

        Args:
            key (str): The dictionary key to use for demoting.
            factor (float): The factor to divide the score by.

        Returns:
            FYPBuilder: The builder instance for chaining methods.
        """
        self._steps.append(('demote_by_key', {'key': key, 'factor': factor}))
        return self

    def boost_recency(self, factor, time_key='timestamp'):
        """Adds a rule to boost items based on their recency.

        Args:
            factor (float): The factor to apply to the recency score.
            time_key (str, optional): The key containing the timestamp. Defaults to 'timestamp'.

        Returns:
            FYPBuilder: The builder instance for chaining methods.
        """
        self._steps.append(('boost_recency', {'factor': factor, 'time_key': time_key}))
        return self

    def sort_by(self, key, reverse=True):
        """Adds a final sorting step to the algorithm, overriding the default score-based sort.

        Args:
            key (str): The dictionary key to sort the items by.
            reverse (bool, optional): Whether to sort in descending order. Defaults to True.

        Returns:
            FYPBuilder: The builder instance for chaining methods.
        """
        self._sort_params = {'key': key, 'reverse': reverse}
        return self

    def limit(self, count):
        """Adds a step to limit the number of returned items.

        Args:
            count (int): The maximum number of items to return.

        Returns:
            FYPBuilder: The builder instance for chaining methods.
        """
        self._steps.append(('limit', {'count': count}))
        return self

    async def run(self):
        """Asynchronously executes the configured algorithm and returns the processed items.

        The rules are executed in the order they were added, and the final list of items
        is sorted by score in descending order.

        Returns:
            list: A list of processed and sorted items.
        """
        for step, params in self._steps:
            if step == 'match_tags':
                tags_to_match = set(params.get('tags', []))
                weight = params.get('weight', 1.0)
                for item in self.items:
                    num_matches = len(tags_to_match.intersection(item.get('tags', [])))
                    if num_matches > 0:
                        self._scores[item['id']] += (weight * num_matches)

            elif step == 'boost_by_key':
                key = params['key']
                factor = params['factor']
                for item in self.items:
                    value = item.get(key, 0)
                    if isinstance(value, (int, float)):
                        self._scores[item['id']] *= (1 + math.log(1 + value) * factor)

            elif step == 'demote_by_key':
                key = params['key']
                factor = params['factor']
                for item in self.items:
                    value = item.get(key, 0)
                    if isinstance(value, (int, float)):
                        self._scores[item['id']] /= (1 + math.log(1 + value) * factor)

            elif step == 'boost_recency':
                factor = params['factor']
                time_key = params['time_key']
                current_time = time.time()
                for item in self.items:
                    item_time = item.get(time_key, current_time)
                    age_seconds = current_time - item_time
                    age_days = age_seconds / (24 * 3600)
                    recency_score = 1 / (1 + age_days)  # Simple recency score
                    self._scores[item['id']] *= (1 + recency_score * factor)

        # Add scores to items
        for item in self.items:
            item['_score'] = self._scores[item['id']]

        # Sort by the specified key or by score as a fallback
        if self._sort_params:
            key = self._sort_params['key']
            reverse = self._sort_params['reverse']
            processed_items = sorted(self.items, key=lambda x: x.get(key, 0), reverse=reverse)
        else:
            processed_items = sorted(self.items, key=lambda x: x['_score'], reverse=True)

        # Apply limit if it's the last step
        limit_step = next((step for step in self._steps if step[0] == 'limit'), None)
        if limit_step:
            count = limit_step[1]['count']
            processed_items = processed_items[:count]

        return processed_items
