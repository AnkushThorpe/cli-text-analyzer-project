# CLI Text Analyzer
![tests](https://github.com/AnkushThorpe/cli-text-analyzer-project/actions/workflows/tests.yml/badge.svg)

A small command-line tool that reads a text file and reports:

- **Total word count**
- **Most common words**, with common stopwords ("the", "and", "is", …) excluded
- **Average sentence length**, in words

Written in plain Python with no third-party dependencies.

## Requirements

- Python 3.8 or newer
- `pytest` (only needed to run the tests)

## Usage

```bash
python project_text_analyzer.py sample_text.txt
```

Show a different number of top words with `--top`:

```bash
python project_text_analyzer.py sample_text.txt --top 3
```

Run `python project_text_analyzer.py --help` to see all options.

## Example output

Running it on the included `sample_text.txt`:

```text
Total words: 79
Top 10 words (stopwords excluded):
  code: 6
  read: 4
  write: 4
  clear: 3
  easy: 3
  python: 2
  readability: 2
  works: 2
  dynamic: 1
  interpreted: 1
Average sentence length: 8.78 words
```

## How it works

1. **Words.** The text is split on whitespace. Each token is lowercased and has punctuation stripped from its ends with a regex, so `"Code,"` and `"code"` count as the same word. Tokens that are only punctuation (like `—` or `...`) are not counted.
2. **Top words.** Stopwords are filtered out and the rest are counted with `collections.Counter`.
3. **Sentences.** The text is split on `.`, `!` and `?`. Empty pieces left by repeated punctuation (`"Wait!!!"`) are ignored, and the average is rounded to two decimals.

## Running the tests

```bash
pip install pytest
python -m pytest
```

The tests cover empty input, punctuation-only tokens, case-insensitive counting, the `--top` limit and repeated punctuation.

## Limitations

- Sentence splitting is naive: abbreviations like "e.g." or "Dr." and decimals like "3.14" are treated as sentence breaks.
- The stopword list is short and English-only.
- Hyphenated words ("well-known") are counted as a single word.

## Project structure

```text
project_text_analyzer.py   # analysis logic and command-line interface
test_text_analyzer.py      # pytest tests
sample_text.txt            # example input
```
