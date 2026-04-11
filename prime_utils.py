"""Compatibility wrapper for PrimeHunter prime helpers."""

from primehunter.math_core.primes import (
    all_primes_below,
    generate_primes,
    is_prime,
    parse_seed_primes,
    prime_factorization,
    prime_factors,
    smallest_prime_factor,
)

__all__ = [
    "all_primes_below",
    "generate_primes",
    "is_prime",
    "parse_seed_primes",
    "prime_factorization",
    "prime_factors",
    "smallest_prime_factor",
]
