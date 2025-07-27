from collections import Counter

class Pattern:
    """Manages user interest patterns by learning from their interactions."""
    def __init__(self):
        """Initializes the Pattern learner with an empty dictionary for user patterns."""
        self.user_patterns = {}

    async def learn(self, user_id, interests):
        """Asynchronously learns and updates the interest pattern for a specific user.

        This method takes a list of interests (e.g., tags, keywords) and updates
        the user's profile, incrementing the counts for each interest.

        Args:
            user_id (any): The unique identifier for the user.
            interests (list): A list of strings representing the user's interests.

        Raises:
            TypeError: If the interests are not provided as a list.
        """
        if not isinstance(interests, list):
            raise TypeError("Interests must be a list of tags or keywords.")

        if user_id not in self.user_patterns:
            self.user_patterns[user_id] = Counter()

        self.user_patterns[user_id].update(interests)

    async def auto_learn(self, user_id, tags):
        """Asynchronously learns from user behavior, acting as an alias for the `learn` method.

        This method is designed for implicitly tracking user interactions, such as
        clicking on an item with certain tags.

        Args:
            user_id (any): The unique identifier for the user.
            tags (list): A list of tags associated with an item the user interacted with.
        """
        return await self.learn(user_id, tags)

    async def get_pattern(self, user_id):
        """Asynchronously retrieves the learned interest pattern for a user.

        Args:
            user_id (any): The unique identifier for the user.

        Returns:
            collections.Counter: A Counter object representing the user's interests and their scores.
                                 Returns an empty Counter if the user has no pattern.
        """
        return self.user_patterns.get(user_id, Counter())

    async def get_all_patterns(self):
        """Asynchronously retrieves all learned user patterns.

        Returns:
            dict: A dictionary where keys are user IDs and values are Counter objects
                  representing their interest patterns.
        """
        return self.user_patterns
