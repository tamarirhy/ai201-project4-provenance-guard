def calculate_confidence(
    llm_score,
    stylometry_score,
    burstiness_score
):
    """
    Combine all three detection signals into one
    confidence score.

    Weights:
    LLM = 50%
    Stylometry = 30%
    Burstiness = 20%
    """

    confidence = (
        llm_score * 0.50 +
        stylometry_score * 0.30 +
        burstiness_score * 0.20
    )

    return round(confidence, 2)