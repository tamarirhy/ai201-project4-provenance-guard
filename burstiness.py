import re
import statistics


def analyze_burstiness(text):
    """
    Measures how much sentence lengths vary.

    Human writing tends to have greater variation
    in sentence lengths, while AI writing is often
    more uniform.

    Returns:
    {
        "score": float (0.0 - 1.0)
    }

    Higher score = more AI-like
    """

    sentences = [
        s.strip()
        for s in re.split(r"[.!?]+", text)
        if s.strip()
    ]

    if len(sentences) < 2:
        return {"score": 0.5}

    lengths = [len(s.split()) for s in sentences]

    variance = statistics.pvariance(lengths)

    # Low variance → more AI-like
    score = max(0, min(1, 1 - (variance / 100)))

    return {
        "score": round(score, 2)
    }