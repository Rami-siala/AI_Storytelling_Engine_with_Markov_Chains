## AI_Storytelling_Engine_with_Markov_Chains

Feed the program classic public-domain text (hardcoded excerpts defined in code) and build a Markov Chain text generator from scratch with pure Python. Let users pick a "style" and generate original story paragraphs.

**Features:**
- Multiple hardcoded text styles (Shakespearean, Gothic horror, fairy tale, sci-fi) defined as string constants
- Markov chain builder from scratch (configurable n-gram order: bigram, trigram)
- Style selector — pick a genre and generate paragraphs in that voice
- Adjustable creativity slider (chain order affects coherence vs. novelty)
- Seed word input — start the story with a word of your choice
- Side-by-side comparison of outputs from different chain orders

**Masters Skills:**
- Markov chains from scratch (transition matrices, n-grams)
- Probabilistic text generation
- N-gram language modeling fundamentals
- Understanding the creativity-coherence tradeoff

**Tools:**
- `random` — weighted random selection from transition probabilities
- `collections` — defaultdict for building chain dictionaries
- `re` — text tokenization and cleaning
- `textwrap` — formatted paragraph output
- `json` — save/load trained chain models



