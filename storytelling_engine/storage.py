"""
Model persistence for the AI Storytelling Engine.

Saves and loads trained Markov chain models as JSON files.
Handles the tuple-key serialization problem by joining/splitting
key tuples with a pipe delimiter.
"""

import json
import os

SAVE_DIR = "saved_models"


def save_chain(chain, style_name, order):
    """
    Save a trained chain to a JSON file.

    Converts tuple keys to pipe-delimited strings for JSON compatibility.
    Files are stored as {style_name}_order{order}.json in SAVE_DIR.

    Args:
        chain:      transition dictionary from build_chain()
        style_name: style key (e.g. "fairy_tale")
        order:      chain order used when building

    Returns:
        filepath of the saved model
    """
    os.makedirs(SAVE_DIR, exist_ok=True)
    filename = f"{style_name}_order{order}.json"
    filepath = os.path.join(SAVE_DIR, filename)

    # Convert tuple keys to JSON-compatible string keys
    serializable = {"|".join(k): v for k, v in chain.items()}

    with open(filepath, "w") as f:
        json.dump(serializable, f)

    print(f"Model saved to {filepath}")
    return filepath


def load_chain(style_name, order):
    """
    Load a previously saved chain from JSON.

    Converts pipe-delimited string keys back to tuples.

    Args:
        style_name: style key (e.g. "fairy_tale")
        order:      chain order

    Returns:
        transition dictionary, or None if no saved model exists
    """
    filename = f"{style_name}_order{order}.json"
    filepath = os.path.join(SAVE_DIR, filename)

    if not os.path.exists(filepath):
        return None

    with open(filepath, "r") as f:
        data = json.load(f)

    # Convert string keys back to tuples
    chain = {tuple(k.split("|")): v for k, v in data.items()}

    print(f"Model loaded from {filepath}")
    return chain
