"""Compatibility wrapper for reciprocal-cycle PrimeHunter helpers."""

from primehunter.analysis.reciprocal_cycles import (
    BASE_DIGITS,
    DEFAULT_BASES,
    DEFAULT_LIMIT,
    analyze_prime_for_bases,
    build_summary,
    classify_twin_prime,
    format_base_digit,
    multiplicative_order,
    parse_bases,
    reciprocal_expansion,
    run_reciprocal_cycle_experiment,
)
from primehunter.data.reciprocal_cycle_exports import (
    FORMAT_SUFFIXES,
    default_output_path,
    summary_text,
    write_csv,
    write_json,
    write_multiple_formats,
    write_results,
    write_text_report,
)

__all__ = [
    "BASE_DIGITS",
    "DEFAULT_BASES",
    "DEFAULT_LIMIT",
    "FORMAT_SUFFIXES",
    "analyze_prime_for_bases",
    "build_summary",
    "classify_twin_prime",
    "default_output_path",
    "format_base_digit",
    "multiplicative_order",
    "parse_bases",
    "reciprocal_expansion",
    "run_reciprocal_cycle_experiment",
    "summary_text",
    "write_csv",
    "write_json",
    "write_multiple_formats",
    "write_results",
    "write_text_report",
]
