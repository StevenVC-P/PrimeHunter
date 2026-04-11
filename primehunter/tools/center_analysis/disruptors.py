"""Disruptor analysis for composite center candidates."""

from primehunter.math_core.primes import is_prime, prime_factorization, smallest_prime_factor


def smallest_disruptor(value):
    """Return the smallest prime factor for composite values, otherwise None."""
    if value <= 1:
        raise ValueError("value must be greater than 1.")
    return smallest_prime_factor(value)


def full_disruptor_data(value):
    """Return canonical disruptor data for a candidate value."""
    if value <= 1:
        raise ValueError("value must be greater than 1.")

    value_is_prime = is_prime(value)
    return {
        "value": value,
        "is_prime": value_is_prime,
        "smallest_disruptor": None if value_is_prime else smallest_disruptor(value),
        "factorization": prime_factorization(value),
    }


def analyze_composite_side(value):
    """Return canonical side-level data for a composite candidate."""
    data = full_disruptor_data(value)
    if data["is_prime"]:
        raise ValueError("Composite-side analysis requires a composite value.")
    return data
