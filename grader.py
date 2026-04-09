LABEL_SEVERITY = {
    "safe": 0,
    "suspicious": 1,
    "phishing": 2,
}

MIN_SCORE = 0.01
MAX_SCORE = 0.99


def grade(predicted: str, actual: str) -> float:
    """
    Score a predicted label against the ground truth.

    Severity ladder: safe (0) -> suspicious (1) -> phishing (2)
    - MAX_SCORE: exact match
    - 0.5: one step away
    - MIN_SCORE: opposite ends
    """
    if predicted not in LABEL_SEVERITY or actual not in LABEL_SEVERITY:
        raise ValueError(
            f"Invalid label. Got predicted='{predicted}', actual='{actual}'. "
            f"Expected one of: {list(LABEL_SEVERITY.keys())}"
        )

    if predicted == actual:
        return MAX_SCORE

    distance = abs(LABEL_SEVERITY[predicted] - LABEL_SEVERITY[actual])
    return 0.5 if distance == 1 else MIN_SCORE
