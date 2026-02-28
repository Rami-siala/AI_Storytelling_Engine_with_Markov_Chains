"""
Output formatting for the AI Storytelling Engine.

Post-processes raw chain output into readable paragraphs by capitalizing
sentence starts, attaching punctuation to the preceding word, and
wrapping text to a fixed width.
"""

import textwrap


def format_paragraph(text, width=70):
    """
    Format raw generated text into a clean, readable paragraph.

    Post-processing pipeline:
        1. Capitalize the first word and words after sentence-ending marks
        2. Attach sentence-ending punctuation (. ! ?) to the preceding word
        3. Wrap to the specified width with textwrap.fill

    Args:
        text:  raw generated string (lowercase, punctuation as own tokens)
        width: line width for wrapping

    Returns:
        formatted paragraph string
    """
    words = text.split()
    result = []
    capitalize_next = True

    for word in words:
        if capitalize_next and word not in ".!?":
            word = word.capitalize()
            capitalize_next = False
        if word in ".!?":
            # Attach punctuation to previous word
            if result:
                result[-1] = result[-1] + word
            capitalize_next = True
            continue
        result.append(word)

    text = " ".join(result)
    return textwrap.fill(text, width=width)


def display_comparison(text_order2, text_order3, style_name):
    """
    Print two generated texts for side-by-side order comparison.

    Args:
        text_order2:  raw generated text from a bigram chain
        text_order3:  raw generated text from a trigram chain
        style_name:   display label for the style (e.g. "Gothic Horror")
    """
    print(f"\n{'=' * 70}")
    print(f"  COMPARISON: {style_name}")
    print(f"{'=' * 70}")

    print(f"\n--- Order 2 (Bigram) — More Creative ---\n")
    print(format_paragraph(text_order2))

    print(f"\n--- Order 3 (Trigram) — More Coherent ---\n")
    print(format_paragraph(text_order3))

    print(f"\n{'=' * 70}")
