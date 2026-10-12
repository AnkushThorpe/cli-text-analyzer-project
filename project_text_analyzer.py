"""
CLI Text Analyzer

Reads a text file and reports:
    - total word count
    - the most common words (excluding common stopwords)
    - average sentence length, in words

Usage:
    python project_text_analyzer.py sample_text.txt
    python project_text_analyzer.py sample_text.txt --top 5
"""
import argparse
import re
import sys
from collections import Counter

# Matches runs of non-letter/non-digit characters at the start or end of a token.
EDGE_PUNCTUATION = re.compile(r"^[\W_]+|[\W_]+$")

STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "is", "are", "was", "were",
    "in", "on", "at", "to", "of", "it", "this", "that", "with", "as",
}


def clean_word(word: str) -> str:
    """
    Lowercase a word and strip surrounding punctuation ("Code," -> "code").

    Uses a regex instead of string.punctuation so non-ASCII marks such as
    the em dash (—) or curly quotes are stripped too. Inner apostrophes
    ("people's") are kept.
    """
    return EDGE_PUNCTUATION.sub("", word).lower()


def analyze_text(text: str, top_n: int = 10) -> dict:
    """
    Analyze a block of text and return a dict with:
        "total_words": number of words, stopwords included. Tokens made up
            only of punctuation (like "—" or "...") are not counted.
        "top_words": list of (word, count) pairs for the top_n most common
            non-stopword words, most common first.
        "avg_sentence_length": average words per sentence, rounded to
            2 decimals. Sentences end at '.', '!' or '?'; empty pieces from
            repeated or trailing punctuation are ignored.
    """
    # Clean every token once, dropping punctuation-only tokens, so the word
    # count and the frequency list are based on the same definition of a word.
    words = [w for w in (clean_word(t) for t in text.split()) if w]
    total_words = len(words)

    top_words = Counter(w for w in words if w not in STOPWORDS).most_common(top_n)

    sentence_text = text.replace("!", ".").replace("?", ".")
    sentence_lengths = []
    for piece in sentence_text.split("."):
        length = sum(1 for t in piece.split() if clean_word(t))
        if length > 0:
            sentence_lengths.append(length)

    if sentence_lengths:
        avg_sentence_length = round(sum(sentence_lengths) / len(sentence_lengths), 2)
    else:
        avg_sentence_length = 0.0

    return {
        "total_words": total_words,
        "top_words": top_words,
        "avg_sentence_length": avg_sentence_length,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Report word count, most common words and average sentence length for a text file."
    )
    parser.add_argument("path", help="path to a UTF-8 text file")
    parser.add_argument(
        "--top", type=int, default=10, metavar="N",
        help="number of most common words to show (default: 10)",
    )
    args = parser.parse_args()

    if args.top < 1:
        parser.error("--top must be at least 1")

    try:
        with open(args.path, "r", encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Error: file not found: {args.path}", file=sys.stderr)
        sys.exit(1)

    stats = analyze_text(text, top_n=args.top)

    print(f"Total words: {stats['total_words']}")
    print(f"Top {args.top} words (stopwords excluded):")
    for word, count in stats["top_words"]:
        print(f"  {word}: {count}")
    print(f"Average sentence length: {stats['avg_sentence_length']} words")


if __name__ == "__main__":
    main()
