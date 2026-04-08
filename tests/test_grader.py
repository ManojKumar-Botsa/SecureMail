import pytest

from grader import grade


def test_grade_exact_match():
    assert grade("safe", "safe") == 1.0
    assert grade("suspicious", "suspicious") == 1.0
    assert grade("phishing", "phishing") == 1.0


def test_grade_adjacent():
    assert grade("safe", "suspicious") == 0.5
    assert grade("suspicious", "safe") == 0.5
    assert grade("suspicious", "phishing") == 0.5
    assert grade("phishing", "suspicious") == 0.5


def test_grade_opposite():
    assert grade("safe", "phishing") == 0.0
    assert grade("phishing", "safe") == 0.0


def test_grade_invalid_label():
    with pytest.raises(ValueError):
        grade("invalid", "safe")
