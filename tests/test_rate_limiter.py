"""Tests for rate limiter."""

from src.rate_limiter import RateLimiter


def test_rate_limiter_allows_request_under_limit():
    """Request under limit is allowed."""
    limiter = RateLimiter(requests_per_minute=10, requests_per_hour=100)
    assert limiter.check_limit("user1") is True


def test_rate_limiter_blocks_request_over_minute_limit():
    """Request over per-minute limit is blocked."""
    limiter = RateLimiter(requests_per_minute=2, requests_per_hour=100)
    limiter.check_limit("user1")
    limiter.check_limit("user1")
    result = limiter.check_limit("user1")
    assert result is False


def test_rate_limiter_separate_users():
    """Different users have separate limits."""
    limiter = RateLimiter(requests_per_minute=1, requests_per_hour=100)
    assert limiter.check_limit("user1") is True
    assert limiter.check_limit("user2") is True


def test_rate_limiter_tracks_request_count():
    """Request count is tracked per user."""
    limiter = RateLimiter(requests_per_minute=5, requests_per_hour=100)
    for _ in range(5):
        limiter.check_limit("user1")
    result = limiter.check_limit("user1")
    assert result is False


def test_rate_limiter_reset_clears_user():
    """Reset clears user state."""
    limiter = RateLimiter(requests_per_minute=1, requests_per_hour=100)
    limiter.check_limit("user1")
    limiter.reset("user1")
    assert limiter.check_limit("user1") is True


def test_rate_limiter_hourly_limit():
    """Hourly limit is enforced."""
    limiter = RateLimiter(requests_per_minute=100, requests_per_hour=2)
    limiter.check_limit("user1")
    limiter.check_limit("user1")
    result = limiter.check_limit("user1")
    assert result is False


def test_rate_limiter_get_remaining():
    """Get remaining requests for user."""
    limiter = RateLimiter(requests_per_minute=5, requests_per_hour=100)
    limiter.check_limit("user1")
    limiter.check_limit("user1")
    remaining = limiter.get_remaining("user1")
    assert remaining == 3
