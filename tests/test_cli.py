"""Tests for CLI."""

import json
import os
import tempfile
from io import StringIO
from unittest.mock import patch

from src.cli import main


def test_cli_init():
    """Test CLI init command."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as f:
        temp_file = f.name

    try:
        with patch("sys.argv", ["cli", "-c", temp_file, "init", "-r", "30", "--tokens", "5000"]):
            with patch("sys.stdout", new_callable=StringIO):
                result = main()
                assert result == 0
                assert os.path.exists(temp_file)
                with open(temp_file) as f:
                    data = json.load(f)
                assert data["requests_per_minute"] == 30
                assert data["token_budget"] == 5000
    finally:
        os.unlink(temp_file)


def test_cli_show():
    """Test CLI show command."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
        json.dump({"requests_per_minute": 25, "requests_per_hour": 500, "token_budget": 25000}, f)
        temp_file = f.name

    try:
        with patch("sys.argv", ["cli", "-c", temp_file, "show"]):
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                result = main()
                assert result == 0
                output = mock_stdout.getvalue()
                data = json.loads(output)
                assert data["requests_per_minute"] == 25
    finally:
        os.unlink(temp_file)


def test_cli_check_allowed():
    """Test CLI check command - allowed."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
        json.dump({"requests_per_minute": 60, "requests_per_hour": 1000, "token_budget": 100000}, f)
        temp_file = f.name

    try:
        with patch("sys.argv", ["cli", "-c", temp_file, "check", "user1", "100"]):
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                result = main()
                assert result == 0
                assert "Allowed" in mock_stdout.getvalue()
    finally:
        os.unlink(temp_file)


def test_cli_check_blocked():
    """Test CLI check command - blocked by budget."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
        json.dump({"requests_per_minute": 60, "requests_per_hour": 100, "token_budget": 50}, f)
        temp_file = f.name

    try:
        with patch("sys.argv", ["cli", "-c", temp_file, "check", "user1", "100"]):
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                result = main()
                assert result == 1
                assert "Blocked" in mock_stdout.getvalue()
    finally:
        os.unlink(temp_file)


def test_cli_status():
    """Test CLI status command."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
        json.dump({"requests_per_minute": 60, "requests_per_hour": 1000, "token_budget": 100000}, f)
        temp_file = f.name

    try:
        with patch("sys.argv", ["cli", "-c", temp_file, "status", "user1"]):
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                result = main()
                assert result == 0
                output = mock_stdout.getvalue()
                assert "user1" in output
                assert "Remaining requests" in output
    finally:
        os.unlink(temp_file)


def test_cli_reset():
    """Test CLI reset command."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
        json.dump({"requests_per_minute": 60, "requests_per_hour": 1000, "token_budget": 100000}, f)
        temp_file = f.name

    try:
        with patch("sys.argv", ["cli", "-c", temp_file, "check", "user1", "10"]):
            main()

        with patch("sys.argv", ["cli", "-c", temp_file, "reset", "user1"]):
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                result = main()
                assert result == 0
                assert "Reset" in mock_stdout.getvalue()
    finally:
        os.unlink(temp_file)
