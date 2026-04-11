"""Core missing-partner analysis built on center-analysis records."""

from primehunter.tools.center_analysis import analyze_center_range, summarize_center_range
from primehunter.tools.missing_partner_analysis.statistics import build_summary_from_counts


def is_missing_partner_case(record):
    """Return True when exactly one side of the center is prime."""
    return record["classification"] in ("left_only_prime", "right_only_prime")


def extract_missing_partner_cases(records):
    """Return only records where exactly one side is prime."""
    return [record for record in records if is_missing_partner_case(record)]


def analyze_missing_partner_range(start_n, end_n):
    """Analyze an inclusive range and return missing-partner cases only."""
    return extract_missing_partner_cases(analyze_center_range(start_n, end_n))


def summarize_missing_partner_range(start_n, end_n):
    """Return a summary-only missing-partner view for an inclusive range."""
    center_summary = summarize_center_range(start_n, end_n)
    return build_summary_from_counts(
        analyzed_center_count=center_summary["center_count"],
        left_count=center_summary["left_only_prime_count"],
        right_count=center_summary["right_only_prime_count"],
        frequencies=center_summary["smallest_disruptor_frequencies"],
    )
