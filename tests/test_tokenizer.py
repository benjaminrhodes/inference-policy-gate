"""Tests for token counting."""

from src.tokenizer import count_tokens


def test_count_tokens_basic():
    """Count tokens using simple character-based estimator."""
    text = "hello world"
    tokens = count_tokens(text)
    assert tokens == 2


def test_count_tokens_empty():
    """Empty string returns 0 tokens."""
    assert count_tokens("") == 0


def test_count_tokens_multiple_words():
    """Multiple words count correctly."""
    text = "the quick brown fox jumps over the lazy dog"
    tokens = count_tokens(text)
    assert tokens == 9


def test_count_tokens_collapse_whitespace():
    """Multiple whitespace characters collapse to single split."""
    text = "a   b"
    tokens = count_tokens(text)
    assert tokens == 2
