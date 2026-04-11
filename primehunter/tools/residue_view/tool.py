"""Core residue-view analysis built on center-analysis records."""

from primehunter.math_core import is_prime
from primehunter.tools.center_analysis import analyze_center_range

DEFAULT_RESIDUE_PRIMES = (5, 7, 11)
MAX_TRACKED_PRIMES = 6


def normalize_tracked_primes(primes=None):
    """Return a validated small inspection list of tracked primes."""
    residue_primes = list(DEFAULT_RESIDUE_PRIMES if primes is None else primes)
    if not residue_primes:
        raise ValueError("At least one tracked prime must be provided.")
    if len(residue_primes) > MAX_TRACKED_PRIMES:
        raise ValueError(
            f"Tracked primes are limited to {MAX_TRACKED_PRIMES} values in v1."
        )

    seen = set()
    normalized = []
    for prime_value in residue_primes:
        if prime_value in seen:
            raise ValueError(f"Duplicate tracked prime provided: {prime_value}.")
        if prime_value <= 3:
            raise ValueError(
                "Tracked primes in v1 must be primes greater than 3 within the fixed mod-6 model."
            )
        if not is_prime(prime_value):
            raise ValueError(f"Tracked value is not prime: {prime_value}.")
        seen.add(prime_value)
        normalized.append(prime_value)
    return normalized


def _side_residue_view(side_record, primes):
    residues = {}
    eliminated_by = []
    for prime_value in primes:
        residue = side_record["value"] % prime_value
        residues[str(prime_value)] = residue
        if not side_record["is_prime"] and side_record["value"] != prime_value and residue == 0:
            eliminated_by.append(prime_value)

    return {
        "residues": residues,
        "eliminated_by": eliminated_by,
        "smallest_eliminator": eliminated_by[0] if eliminated_by else None,
    }


def build_residue_view_record(center_record, primes=None):
    """Return a derived residue-view record from a canonical center record."""
    residue_primes = normalize_tracked_primes(primes)
    return {
        "n": center_record["n"],
        "center": center_record["center"],
        "classification": center_record["classification"],
        "left": {
            "value": center_record["left"]["value"],
            "is_prime": center_record["left"]["is_prime"],
            **_side_residue_view(center_record["left"], residue_primes),
        },
        "right": {
            "value": center_record["right"]["value"],
            "is_prime": center_record["right"]["is_prime"],
            **_side_residue_view(center_record["right"], residue_primes),
        },
    }


def analyze_residue_view_range(start_n, end_n, primes=None):
    """Analyze an inclusive range of centers into residue-view records."""
    residue_primes = normalize_tracked_primes(primes)
    center_records = analyze_center_range(start_n, end_n)
    return [build_residue_view_record(record, residue_primes) for record in center_records]


def summarize_residue_view_range(start_n, end_n, primes=None):
    """Return a summary-only residue-view analysis for an inclusive range."""
    records = analyze_residue_view_range(start_n, end_n, primes=primes)
    return records
