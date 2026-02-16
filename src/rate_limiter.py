"""Rate limiting using token bucket algorithm."""

import time
from typing import Dict, Any


class RateLimitExceeded(Exception):
    """Raised when rate limit is exceeded."""

    pass


class RateLimiter:
    """Token bucket rate limiter with per-minute and per-hour limits."""

    def __init__(self, requests_per_minute: int = 60, requests_per_hour: int = 1000):
        """Initialize rate limiter.

        Args:
            requests_per_minute: Maximum requests allowed per minute.
            requests_per_hour: Maximum requests allowed per hour.
        """
        self.requests_per_minute = requests_per_minute
        self.requests_per_hour = requests_per_hour
        self._users: Dict[str, Dict[str, Any]] = {}

    def check_limit(self, user_id: str) -> bool:
        """Check if request is allowed for user.

        Args:
            user_id: Unique identifier for the user.

        Returns:
            True if request is allowed, False otherwise.
        """
        current_time = time.time()

        if user_id not in self._users:
            self._users[user_id] = {
                "minute_count": 0,
                "hour_count": 0,
                "minute_reset": current_time + 60,
                "hour_reset": current_time + 3600,
            }

        user = self._users[user_id]

        if current_time >= user["minute_reset"]:
            user["minute_count"] = 0
            user["minute_reset"] = current_time + 60

        if current_time >= user["hour_reset"]:
            user["hour_count"] = 0
            user["hour_reset"] = current_time + 3600

        if user["minute_count"] >= self.requests_per_minute:
            return False

        if user["hour_count"] >= self.requests_per_hour:
            return False

        user["minute_count"] += 1
        user["hour_count"] += 1

        return True

    def get_remaining(self, user_id: str) -> int:
        """Get remaining requests for user in current window.

        Args:
            user_id: Unique identifier for the user.

        Returns:
            Remaining requests in the more restrictive window.
        """
        if user_id not in self._users:
            return min(self.requests_per_minute, self.requests_per_hour)

        user = self._users[user_id]
        minute_remaining = self.requests_per_minute - user["minute_count"]
        hour_remaining = self.requests_per_hour - user["hour_count"]

        return min(minute_remaining, hour_remaining)

    def reset(self, user_id: str) -> None:
        """Reset rate limit for a user.

        Args:
            user_id: Unique identifier for the user.
        """
        if user_id in self._users:
            del self._users[user_id]
