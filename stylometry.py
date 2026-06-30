import re
import statistics
import string


def analyze_stylometry(text):
    """
    Analyze writing style using simple heuristics.

    Returns:
    {
        "score": float (0.0 - 1.0)
    }

    Higher score = more AI-like
    """

    # Split into sentences
    sentences = [
        s.strip() for s in re.split(r"[.!?]+", text) if s.strip()
    ]

    if len(sentences) < 2:
        return {"score": 0.5}

    # -----------------------------
    # Sentence Length Variance
    # -----------------------------
    sentence_lengths = [
        len(sentence.split()) for sentence in sentences
    ]

    variance = statistics.pvariance(sentence_lengths)

    # Lower variance is considered more AI-like
    variance_score = max(0, min(1, 1 - (variance / 50)))

    # -----------------------------
    # Vocabulary Diversity
    # -----------------------------
    words = re.findall(r"\b\w+\b", text.lower())

    if not words:
        return {"score": 0.5}

    unique_words = len(set(words))
    ttr = unique_words / len(words)

    # AI often has moderate vocabulary diversity
    vocab_score = max(0, min(1, 1 - abs(ttr - 0.50) * 2))

    # -----------------------------
    # Punctuation Density
    # -----------------------------
    punctuation_count = sum(
        1 for char in text if char in string.punctuation
    )

    punctuation_density = punctuation_count / len(text)

    punctuation_score = max(
        0,
        min(1, 1 - abs(punctuation_density - 0.05) * 10)
    )

    # -----------------------------
    # Combine the metrics
    # -----------------------------
    score = (
        variance_score +
        vocab_score +
        punctuation_score
    ) / 3

    return {
        "score": round(score, 2)
    }