"""Canonical record builders for twin-prime center analysis."""

from primehunter.tools.center_analysis.classification import classify_center
from primehunter.tools.center_analysis.disruptors import full_disruptor_data


def build_side_record(value):
    """Return the canonical side record."""
    return full_disruptor_data(value)


def build_center_record(n):
    """Return the canonical center record for one twin-prime center."""
    if n < 1:
        raise ValueError("n must be at least 1.")

    center = 6 * n
    left = build_side_record(center - 1)
    right = build_side_record(center + 1)

    return {
        "n": n,
        "center": center,
        "classification": classify_center(left["is_prime"], right["is_prime"]),
        "left": left,
        "right": right,
    }


def build_center_record_from_analysis(center_analysis):
    """Normalize already-computed analysis into the canonical record shape."""
    return {
        "n": center_analysis["n"],
        "center": center_analysis["center"],
        "classification": center_analysis["classification"],
        "left": center_analysis["left"],
        "right": center_analysis["right"],
    }
