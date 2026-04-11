"""Canonical twin-center analysis for PrimeHunter v1."""

from primehunter.tools.center_analysis.records import build_center_record
from primehunter.tools.center_analysis.statistics import (
    build_empty_summary,
    finalize_summary,
    update_summary,
)


def generate_centers(start_n, end_n):
    """Return centers of the form 6n for the inclusive range [start_n, end_n]."""
    if start_n < 1:
        raise ValueError("start_n must be at least 1.")
    if end_n < start_n:
        raise ValueError("end_n must be greater than or equal to start_n.")
    return [6 * n for n in range(start_n, end_n + 1)]


def build_center_candidates(n):
    """Return the center and its paired candidates."""
    if n < 1:
        raise ValueError("n must be at least 1.")
    center = 6 * n
    return {
        "n": n,
        "center": center,
        "left_value": center - 1,
        "right_value": center + 1,
    }


def analyze_center(n):
    """Perform canonical center analysis for one value of n."""
    return build_center_record(n)


def analyze_center_range(start_n, end_n):
    """Analyze an inclusive range of twin-prime centers."""
    if start_n < 1:
        raise ValueError("start_n must be at least 1.")
    if end_n < start_n:
        raise ValueError("end_n must be greater than or equal to start_n.")
    return [analyze_center(n) for n in range(start_n, end_n + 1)]


def summarize_center_range(start_n, end_n):
    """Return a summary-only analysis for an inclusive range of centers."""
    if start_n < 1:
        raise ValueError("start_n must be at least 1.")
    if end_n < start_n:
        raise ValueError("end_n must be greater than or equal to start_n.")

    summary = build_empty_summary()
    for n in range(start_n, end_n + 1):
        update_summary(summary, analyze_center(n))
    return finalize_summary(summary)
