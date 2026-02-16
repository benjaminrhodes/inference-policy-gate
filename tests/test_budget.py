"""Tests for budget manager."""

from src.budget import BudgetManager


def test_budget_manager_allows_request_under_budget():
    """Request under budget is allowed."""
    manager = BudgetManager(token_budget=1000)
    assert manager.check_budget("user1", 500) is True


def test_budget_manager_blocks_request_over_budget():
    """Request over budget is blocked."""
    manager = BudgetManager(token_budget=1000)
    result = manager.check_budget("user1", 1001)
    assert result is False


def test_budget_manager_tracks_spent():
    """Spent tokens are tracked."""
    manager = BudgetManager(token_budget=1000)
    manager.check_budget("user1", 500)
    manager.check_budget("user1", 300)
    remaining = manager.get_remaining("user1")
    assert remaining == 200


def test_budget_manager_separate_users():
    """Different users have separate budgets."""
    manager = BudgetManager(token_budget=1000)
    manager.check_budget("user1", 500)
    assert manager.get_remaining("user1") == 500
    assert manager.get_remaining("user2") == 1000


def test_budget_manager_reset():
    """Reset clears user budget."""
    manager = BudgetManager(token_budget=1000)
    manager.check_budget("user1", 500)
    manager.reset("user1")
    assert manager.get_remaining("user1") == 1000


def test_budget_manager_get_spent():
    """Get spent amount for user."""
    manager = BudgetManager(token_budget=1000)
    manager.check_budget("user1", 400)
    spent = manager.get_spent("user1")
    assert spent == 400


def test_budget_manager_exact_budget():
    """Exact budget usage is allowed."""
    manager = BudgetManager(token_budget=1000)
    assert manager.check_budget("user1", 1000) is True
