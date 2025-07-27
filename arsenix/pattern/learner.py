from collections import Counter

class Pattern:
    def __init__(self):
        self.user_patterns = {}

    async def learn(self, user_id, interests):
        """Learns and updates the interest pattern for a specific user."""
        if not isinstance(interests, list):
            raise TypeError("Interests must be a list of tags or keywords.")

        if user_id not in self.user_patterns:
            self.user_patterns[user_id] = Counter()

        self.user_patterns[user_id].update(interests)

    async def get_pattern(self, user_id):
        """Retrieves the learned interest pattern for a user."""
        return self.user_patterns.get(user_id, Counter())

    async def get_all_patterns(self):
        """Returns all learned user patterns."""
        return self.user_patterns
