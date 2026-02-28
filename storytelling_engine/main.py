"""
CLI entry point for the AI Storytelling Engine.

Provides an interactive menu-driven interface that lets the user
select a writing style, configure chain order, provide a seed word,
generate story paragraphs, compare orders, and save/load models.
"""

from storytelling_engine.corpus import STYLES
from storytelling_engine.tokenizer import tokenize
from storytelling_engine.markov_chain import build_chain, generate_text
from storytelling_engine.storage import save_chain, load_chain
from storytelling_engine.display import format_paragraph, display_comparison

STYLE_LIST = list(STYLES.keys())
STYLE_LABELS = {
    "shakespearean": "Shakespearean",
    "gothic_horror": "Gothic Horror",
    "fairy_tale": "Fairy Tale",
    "sci_fi": "Sci-Fi",
}


def select_style():
    """Display style menu and return the chosen style key."""
    print("\nAvailable styles:")
    for i, key in enumerate(STYLE_LIST, 1):
        print(f"  {i}. {STYLE_LABELS[key]}")

    while True:
        choice = input(f"\nPick a style [1-{len(STYLE_LIST)}]: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(STYLE_LIST):
            return STYLE_LIST[int(choice) - 1]
        print("Invalid choice. Try again.")


def get_order():
    """Prompt for chain order (2 or 3)."""
    choice = input("Chain order (2=bigram, 3=trigram) [2]: ").strip()
    if choice == "3":
        return 3
    return 2


def get_seed():
    """Prompt for optional seed word."""
    seed = input("Seed word (or press Enter for random): ").strip()
    return seed if seed else None


def get_word_count():
    """Prompt for number of words to generate."""
    choice = input("Words to generate [100]: ").strip()
    if choice.isdigit() and int(choice) > 0:
        return int(choice)
    return 100


def get_or_build_chain(style, order):
    """Load a saved chain or build a new one."""
    chain = load_chain(style, order)
    if chain:
        return chain

    print(f"Building {STYLE_LABELS[style]} chain (order={order})...")
    tokens = tokenize(STYLES[style])
    chain = build_chain(tokens, order)
    print(f"Chain built: {len(chain)} states")
    return chain


def main():
    print("=" * 40)
    print("  AI Storytelling Engine")
    print("=" * 40)

    while True:
        # --- Setup ---
        style = select_style()
        order = get_order()
        chain = get_or_build_chain(style, order)

        # --- Action loop ---
        while True:
            seed = get_seed()
            num_words = get_word_count()

            text = generate_text(chain, order, num_words, seed)
            label = STYLE_LABELS[style]

            print(f"\n--- Generated Story ({label}, order={order}) ---\n")
            print(format_paragraph(text))
            print()

            # Post-generation menu
            print("[G]enerate again  [C]ompare orders  [S]ave model  [N]ew style  [Q]uit")
            action = input("Action: ").strip().lower()

            if action == "q":
                print("Goodbye!")
                return
            elif action == "n":
                break  # Back to style selection
            elif action == "s":
                save_chain(chain, style, order)
            elif action == "c":
                # Build the other order for comparison
                other_order = 3 if order == 2 else 2
                other_chain = get_or_build_chain(style, other_order)
                text_current = generate_text(chain, order, num_words, seed)
                text_other = generate_text(other_chain, other_order, num_words, seed)
                if order == 2:
                    display_comparison(text_current, text_other, label)
                else:
                    display_comparison(text_other, text_current, label)
            # "g" or anything else → loops back to generate again


if __name__ == "__main__":
    main()
