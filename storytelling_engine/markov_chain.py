"""
Markov chain builder and text generator for the AI Storytelling Engine.

Builds transition dictionaries from tokenized text using configurable
n-gram order. Uses defaultdict(list) so that random.choice() on the
value lists gives naturally weighted random selection.
"""

import random
from collections import defaultdict


def build_chain(tokens, order=2):
    """
    Build a Markov chain from a token list.

    Slides a window of size `order` across the tokens. For each window
    position, records the next word in a list keyed by the window tuple.
    Duplicate entries in the list act as implicit frequency weights.

    Args:
        tokens: list of word tokens (from tokenizer.tokenize)
        order:  number of words per state (2=bigram, 3=trigram)

    Returns:
        dict mapping tuples of `order` words to lists of possible next words
    """
    chain = defaultdict(list)

    for i in range(len(tokens) - order):
        state = tuple(tokens[i : i + order])
        next_word = tokens[i + order]
        chain[state].append(next_word)

    return dict(chain)


def generate_text(chain, order, num_words=100, seed=None):
    """
    Generate text by walking the Markov chain.

    Picks a starting state (matching the seed word if provided, otherwise
    random), then repeatedly looks up the current state and randomly
    selects a next word. On dead ends, jumps to a random state to keep
    generation flowing.

    Args:
        chain:     transition dictionary from build_chain()
        order:     chain order (must match the order used to build)
        num_words: number of words to generate
        seed:      optional starting word (finds a state that begins with it)

    Returns:
        string of generated text
    """
    if not chain:
        return ""

    # Choose starting state
    if seed:
        # Find all states that start with the seed word
        matching = [k for k in chain.keys() if k[0] == seed.lower()]
        if matching:
            state = random.choice(matching)
        else:
            # Seed not found — fall back to random
            state = random.choice(list(chain.keys()))
    else:
        state = random.choice(list(chain.keys()))

    output = list(state)

    for _ in range(num_words - order):
        next_words = chain.get(state)
        if next_words is None:
            # Dead end — pick a new random state to continue
            state = random.choice(list(chain.keys()))
            continue
        next_word = random.choice(next_words)
        output.append(next_word)
        # Shift the window forward
        state = tuple(output[-order:])

    return " ".join(output)
