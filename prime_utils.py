"""Compatibility wrapper for PrimeHunter prime helpers."""

from primehunter.math_core.primes import (
    all_primes_below,
    is_prime,
    parse_seed_primes,
    prime_factors,
)

__all__ = [
    "all_primes_below",
    "is_prime",
    "parse_seed_primes",
    "prime_factors",
]
