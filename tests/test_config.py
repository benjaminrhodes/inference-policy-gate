"""Tests for config persistence."""

import os
import tempfile
from src.config import Config, load_config, save_config


def test_config_defaults():
    """Default config values."""
    config = Config()
    assert config.requests_per_minute == 60
    assert config.requests_per_hour == 1000
    assert config.token_budget == 100000
    assert config.config_file == "rate_limit_config.json"


def test_config_custom_values():
    """Custom config values."""
    config = Config(
        requests_per_minute=10, requests_per_hour=100, token_budget=5000, config_file="custom.json"
    )
    assert config.requests_per_minute == 10
    assert config.requests_per_hour == 100
    assert config.token_budget == 5000
    assert config.config_file == "custom.json"


def test_save_and_load_config():
    """Save and load config from file."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
        temp_file = f.name

    try:
        config = Config(requests_per_minute=25, requests_per_hour=500, token_budget=25000)
        save_config(config, temp_file)

        loaded = load_config(temp_file)
        assert loaded.requests_per_minute == 25
        assert loaded.requests_per_hour == 500
        assert loaded.token_budget == 25000
    finally:
        os.unlink(temp_file)


def test_load_config_missing_file():
    """Missing config file returns defaults."""
    config = load_config("nonexistent_file.json")
    assert config.requests_per_minute == 60


def test_config_to_dict():
    """Config converts to dict."""
    config = Config(requests_per_minute=30)
    d = config.to_dict()
    assert d["requests_per_minute"] == 30
