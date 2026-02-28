"""
Text tokenizer for the AI Storytelling Engine.

Cleans raw text and splits it into lowercase word tokens,
keeping sentence-ending punctuation as separate tokens so
the Markov chain can learn sentence boundaries.
"""

import re


def tokenize(text):
    """
    Convert raw text into a list of lowercase word tokens.

    Processing pipeline:
        1. Separate sentence-ending punctuation (. ! ?) from words
        2. Remove all other punctuation (commas, semicolons, quotes, etc.)
        3. Lowercase and split on whitespace

    Args:
        text: raw input string

    Returns:
        list of lowercase word tokens (sentence marks kept as own tokens)
    """
    if not text or not text.strip():
        return []

    # Separate sentence-ending punctuation from words
    text = re.sub(r'([.!?])', r' \1', text)

    # Remove all other punctuation (commas, semicolons, quotes, etc.)
    text = re.sub(r'[^a-zA-Z0-9.!?\s]', '', text)

    # Lowercase and split on whitespace
    tokens = text.lower().split()

    return tokens
