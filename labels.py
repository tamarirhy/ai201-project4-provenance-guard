def get_transparency_label(confidence):
    """
    Return the transparency label based on the confidence score.
    """

    if confidence >= 0.65:
        return (
            "Our system believes this content was likely generated using AI. "
            "Multiple indicators support this result, although automated "
            "detection is never perfect."
        )

    elif confidence >= 0.36:
        return (
            "Our system cannot confidently determine whether this content "
            "was written by a person or generated using AI. "
            "Additional review may be necessary."
        )

    else:
        return (
            "Our system believes this content was likely written by a person. "
            "While no automated system is perfect, this submission shows "
            "several characteristics commonly associated with human writing."
        )