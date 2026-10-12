"""
Mini-Project: CLI Text Analyzer

Usage:
    python project_text_analyzer.py sample_text.txt

Reads a text file and reports:
    - total word count
    - the 10 most common words (excluding common stopwords)
    - average sentence length, in words

The CLI plumbing (argument handling, file reading, printing) is done for
you below. Your job is to implement `analyze_text`.
"""
import sys
import string
from collections import Counter

STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "is", "are", "was", "were",
    "in", "on", "at", "to", "of", "it", "this", "that", "with", "as",
}


def analyze_text(text: str) -> dict:
    """
    Return a dict with exactly these keys:
        "total_words": int
            Total number of words in the text (stopwords included).
        "top_10_words": list[tuple[str, int]]
            The 10 most common words, EXCLUDING STOPWORDS, most common first.
            Use collections.Counter.most_common().
        "avg_sentence_length": float
            Average number of words per sentence, rounded to 2 decimals.
            Split sentences on '.', '!', '?'. Ignore empty sentences
            (e.g. from trailing punctuation or multiple punctuation marks).
    """
    # 1. Total words: stopwords included
    total_words = len(text.split())

    # 2. Top 10 words: clean each word, skip empty words and stopwords
    clean_words = []
    for word in text.split():
        word = word.strip(string.punctuation).lower()
        if word and word not in STOPWORDS:
            clean_words.append(word)
    top_10_words = Counter(clean_words).most_common(10)

    # 3. Average sentence length: split on . ! ? and skip empty sentences
    sentence_text = text.replace("!", ".").replace("?", ".")
    sentence_count = 0
    sentence_word_count = 0
    for piece in sentence_text.split("."):
        words = piece.split()
        if len(words) > 0:
            sentence_count += 1
            sentence_word_count += len(words)

    if sentence_count == 0:
        avg_sentence_length = 0.0
    else:
        avg_sentence_length = round(sentence_word_count / sentence_count, 2)

    return {
        "total_words": total_words,
        "top_10_words": top_10_words,
        "avg_sentence_length": avg_sentence_length,
    }


def main():
    if len(sys.argv) != 2:
        print("Usage: python project_text_analyzer.py <path_to_text_file>")
        sys.exit(1)

    path = sys.argv[1]
    try:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Error: file not found: {path}")
        sys.exit(1)

    stats = analyze_text(text)

    print(f"Total words: {stats['total_words']}")
    print("Top 10 words (stopwords excluded):")
    for word, count in stats["top_10_words"]:
        print(f"  {word}: {count}")
    print(f"Average sentence length: {stats['avg_sentence_length']} words")


if __name__ == "__main__":
    main()
