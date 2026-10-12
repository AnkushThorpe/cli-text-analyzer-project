from project_text_analyzer import analyze_text


def test_empty_text():
    stats = analyze_text("")
    assert stats["total_words"] == 0
    assert stats["top_words"] == []
    assert stats["avg_sentence_length"] == 0.0


def test_punctuation_only_tokens_are_not_words():
    stats = analyze_text("Wait ... what — really?")
    assert stats["total_words"] == 3


def test_word_count_includes_stopwords():
    stats = analyze_text("The cat sat on the mat.")
    assert stats["total_words"] == 6


def test_top_words_exclude_stopwords_and_ignore_case():
    stats = analyze_text("Code is fun. CODE is hard. The code works.")
    assert stats["top_words"][0] == ("code", 3)
    assert all(word not in {"is", "the"} for word, _ in stats["top_words"])


def test_top_n_limits_results():
    stats = analyze_text("a b c d e f g h", top_n=3)
    assert len(stats["top_words"]) == 3


def test_average_sentence_length():
    # 4 words + 2 words = 6 words over 2 sentences
    stats = analyze_text("I like clear code. Really works!")
    assert stats["avg_sentence_length"] == 3.0


def test_repeated_punctuation_does_not_create_empty_sentences():
    stats = analyze_text("Hello there!!! How are you?? Fine...")
    # sentences: "Hello there" (2), "How are you" (3), "Fine" (1)
    assert stats["avg_sentence_length"] == 2.0
