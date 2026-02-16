"""Budget management for token usage."""

from typing import Dict


class BudgetExceeded(Exception):
    """Raised when budget is exceeded."""

    pass


class BudgetManager:
    """Manages token budgets per user."""

    def __init__(self, token_budget: int = 100000):
        """Initialize budget manager.

        Args:
            token_budget: Default token budget per user.
        """
        self.token_budget = token_budget
        self._spent: Dict[str, int] = {}

    def check_budget(self, user_id: str, tokens: int) -> bool:
        """Check if request is within budget.

        Args:
            user_id: Unique identifier for the user.
            tokens: Number of tokens for the request.

        Returns:
            True if within budget, False otherwise.
        """
        current_spent = self._spent.get(user_id, 0)

        if current_spent + tokens > self.token_budget:
            return False

        self._spent[user_id] = current_spent + tokens
        return True

    def get_remaining(self, user_id: str) -> int:
        """Get remaining token budget for user.

        Args:
            user_id: Unique identifier for the user.

        Returns:
            Remaining tokens in budget.
        """
        spent = self._spent.get(user_id, 0)
        return max(0, self.token_budget - spent)

    def get_spent(self, user_id: str) -> int:
        """Get spent tokens for user.

        Args:
            user_id: Unique identifier for the user.

        Returns:
            Spent tokens.
        """
        return self._spent.get(user_id, 0)

    def reset(self, user_id: str) -> None:
        """Reset budget for a user.

        Args:
            user_id: Unique identifier for the user.
        """
        if user_id in self._spent:
            del self._spent[user_id]
