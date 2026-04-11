"""Residue-view analysis for PrimeHunter v1."""

from .json_outputs import build_result_envelope, write_json_output
from .statistics import build_summary
from .tool import (
    DEFAULT_RESIDUE_PRIMES,
    MAX_TRACKED_PRIMES,
    analyze_residue_view_range,
    normalize_tracked_primes,
    summarize_residue_view_range,
)

__all__ = [
    "DEFAULT_RESIDUE_PRIMES",
    "MAX_TRACKED_PRIMES",
    "analyze_residue_view_range",
    "build_result_envelope",
    "build_summary",
    "normalize_tracked_primes",
    "summarize_residue_view_range",
    "write_json_output",
]
