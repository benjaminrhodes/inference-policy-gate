"""Configuration management with JSON persistence."""

import json
import os


class Config:
    """Configuration for rate limiting and budget."""

    def __init__(
        self,
        requests_per_minute: int = 60,
        requests_per_hour: int = 1000,
        token_budget: int = 100000,
        config_file: str = "rate_limit_config.json",
    ):
        """Initialize config.

        Args:
            requests_per_minute: Max requests per minute per user.
            requests_per_hour: Max requests per hour per user.
            token_budget: Token budget per user.
            config_file: Path to config file for persistence.
        """
        self.requests_per_minute = requests_per_minute
        self.requests_per_hour = requests_per_hour
        self.token_budget = token_budget
        self.config_file = config_file

    def to_dict(self) -> dict:
        """Convert config to dictionary.

        Returns:
            Dictionary representation of config.
        """
        return {
            "requests_per_minute": self.requests_per_minute,
            "requests_per_hour": self.requests_per_hour,
            "token_budget": self.token_budget,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Config":
        """Create config from dictionary.

        Args:
            data: Dictionary with config values.

        Returns:
            Config instance.
        """
        return cls(
            requests_per_minute=data.get("requests_per_minute", 60),
            requests_per_hour=data.get("requests_per_hour", 1000),
            token_budget=data.get("token_budget", 100000),
        )


def save_config(config: Config, filepath: str) -> None:
    """Save config to JSON file.

    Args:
        config: Config to save.
        filepath: Path to save config file.
    """
    with open(filepath, "w") as f:
        json.dump(config.to_dict(), f, indent=2)


def load_config(filepath: str) -> Config:
    """Load config from JSON file.

    Args:
        filepath: Path to config file.

    Returns:
        Config instance, or default config if file doesn't exist.
    """
    if not os.path.exists(filepath):
        return Config()

    with open(filepath, "r") as f:
        data = json.load(f)

    return Config.from_dict(data)
