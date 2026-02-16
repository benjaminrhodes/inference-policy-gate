"""Simple character-based token counter."""


def count_tokens(text: str) -> int:
    """Count tokens using simple word-based estimator.

    Args:
        text: Input text to count tokens for.

    Returns:
        Estimated token count (1 token per word).
    """
    if not text:
        return 0
    return len(text.split())
