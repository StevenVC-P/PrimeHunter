"""Reciprocal-cycle analysis across primes and bases."""

from __future__ import annotations

from math import gcd

from primehunter.math_core.primes import all_primes_below, is_prime, prime_factors

DEFAULT_LIMIT = 1000
DEFAULT_BASES = (6, 12)
BASE_DIGITS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def multiplicative_order(base, prime_value):
    """Return the multiplicative order of base modulo prime_value."""
    if prime_value <= 1:
        raise ValueError("Prime modulus must be greater than 1.")
    if base % prime_value == 0:
        raise ValueError("Base and modulus must be coprime.")

    order = prime_value - 1
    for factor in sorted(set(prime_factors(order))):
        while order % factor == 0 and pow(base, order // factor, prime_value) == 1:
            order //= factor
    return order


def format_base_digit(value):
    """Return a single digit symbol for the supported bases."""
    if not 0 <= value < len(BASE_DIGITS):
        raise ValueError(f"Digit value {value} is out of range.")
    return BASE_DIGITS[value]


def parse_bases(bases_text):
    """Parse a comma-separated base list."""
    if bases_text is None:
        return list(DEFAULT_BASES)

    values = []
    for part in bases_text.split(","):
        text = part.strip()
        if not text:
            continue
        value = int(text)
        if value < 2:
            raise ValueError("Each base must be at least 2.")
        if value > len(BASE_DIGITS):
            raise ValueError(
                f"Each base must be at most {len(BASE_DIGITS)} when expansions are enabled."
            )
        values.append(value)

    if not values:
        raise ValueError("At least one base must be provided.")

    return values


def reciprocal_expansion(prime_value, base):
    """Return the repeating expansion details for 1 / prime_value in the given base."""
    if prime_value <= 1:
        raise ValueError("Prime modulus must be greater than 1.")
    if base % prime_value == 0:
        raise ValueError("Base and modulus must be coprime.")

    seen_remainders = {}
    digits = []
    remainder = 1 % prime_value

    while remainder and remainder not in seen_remainders:
        seen_remainders[remainder] = len(digits)
        remainder *= base
        digit = remainder // prime_value
        digits.append(format_base_digit(digit))
        remainder %= prime_value

    if remainder == 0:
        non_repeating = "".join(digits)
        repeating = ""
    else:
        cycle_start = seen_remainders[remainder]
        non_repeating = "".join(digits[:cycle_start])
        repeating = "".join(digits[cycle_start:])

    expansion_text = f"0.{non_repeating}"
    if repeating:
        expansion_text += f"({repeating})"

    return {
        "base": base,
        "expansion": expansion_text,
        "non_repeating": non_repeating,
        "repeating": repeating,
        "cycle_length": len(repeating),
    }


def classify_twin_prime(prime_value):
    """Return twin-prime membership flags for a prime."""
    has_twin_lower = is_prime(prime_value - 2)
    has_twin_upper = is_prime(prime_value + 2)
    return {
        "has_twin_lower": has_twin_lower,
        "has_twin_upper": has_twin_upper,
        "is_twin_prime": has_twin_lower or has_twin_upper,
    }


def analyze_prime_for_bases(prime_value, bases, include_expansions=False):
    """Return reciprocal-cycle analysis fields for one prime across one or more bases."""
    if prime_value <= 3:
        raise ValueError("This experiment only supports primes greater than 3.")

    twin_flags = classify_twin_prime(prime_value)
    record = {
        "prime": prime_value,
        **twin_flags,
    }

    for base in bases:
        order = multiplicative_order(base, prime_value)
        record[f"base{base}_order"] = order
        record[f"base{base}_ratio"] = round(order / (prime_value - 1), 10)

        if include_expansions:
            expansion = reciprocal_expansion(prime_value, base)
            record[f"base{base}_expansion"] = expansion["expansion"]
            record[f"base{base}_repeating"] = expansion["repeating"]

    return record


def _maximal_order_count(records, base):
    order_key = f"base{base}_order"
    return sum(1 for record in records if record[order_key] == record["prime"] - 1)


def build_summary(records, limit, bases, include_expansions, skipped_primes):
    """Return experiment-level summary fields for reciprocal-cycle analysis."""
    twin_records = [record for record in records if record["is_twin_prime"]]

    maximal_order_counts = {}
    for base in bases:
        maximal_order_counts[f"base{base}_overall"] = _maximal_order_count(records, base)
        maximal_order_counts[f"base{base}_twin_primes"] = _maximal_order_count(
            twin_records, base
        )

    return {
        "limit": limit,
        "bases": list(bases),
        "analyzed_prime_count": len(records),
        "skipped_primes": skipped_primes,
        "include_expansions": include_expansions,
        "twin_prime_count": len(twin_records),
        "maximal_order_counts": maximal_order_counts,
    }


def run_reciprocal_cycle_experiment(limit, bases=None, include_expansions=False):
    """Analyze reciprocal cycles for primes below limit in one or more bases."""
    normalized_bases = list(DEFAULT_BASES if bases is None else bases)
    analyzed_primes = [
        prime_value
        for prime_value in all_primes_below(limit)
        if not (
            prime_value <= 3
            or any(gcd(base, prime_value) != 1 for base in normalized_bases)
        )
    ]
    skipped_primes = [
        prime_value
        for prime_value in all_primes_below(limit)
        if prime_value <= 3 or any(gcd(base, prime_value) != 1 for base in normalized_bases)
    ]
    records = [
        analyze_prime_for_bases(
            prime_value,
            normalized_bases,
            include_expansions=include_expansions,
        )
        for prime_value in analyzed_primes
    ]
    return {
        "experiment": "reciprocal_cycle_structure",
        "bases": normalized_bases,
        "summary": build_summary(
            records,
            limit,
            normalized_bases,
            include_expansions,
            skipped_primes,
        ),
        "primes": records,
    }
