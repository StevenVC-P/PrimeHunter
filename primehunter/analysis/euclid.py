"""Euclid-style prime discovery analysis."""

from __future__ import annotations

from primehunter.math_core.primes import (
    all_primes_below,
    is_prime,
    parse_seed_primes,
    prime_factors,
)

DEFAULT_LIMIT = 1000
DEFAULT_SEED = [2]

MODE_CONFIGS = {
    "full": {
        "allow_repeated_factors": True,
        "factor_composites": True,
        "short_label": "full",
        "description": "Repeated factors allowed; factor composite results.",
    },
    "square_free_factor": {
        "allow_repeated_factors": False,
        "factor_composites": True,
        "short_label": "square_free_factor",
        "description": "Square-free products only; factor composite results.",
    },
    "square_free_no_factor": {
        "allow_repeated_factors": False,
        "factor_composites": False,
        "short_label": "square_free_no_factor",
        "description": "Square-free products only; keep only prime N + 1 results.",
    },
}


def get_mode_config(mode_name):
    """Return the mode configuration for a named experiment mode."""
    if mode_name not in MODE_CONFIGS:
        known = ", ".join(sorted(MODE_CONFIGS))
        raise ValueError(f"Unknown mode '{mode_name}'. Expected one of: {known}")
    return MODE_CONFIGS[mode_name].copy()


def parse_seed(seed_text, default_seed=None):
    """Parse a seed string, falling back to the configured default."""
    if seed_text is None:
        return list(DEFAULT_SEED if default_seed is None else default_seed)
    return parse_seed_primes(seed_text)


def format_combination(exponents):
    """Format a prime-exponent map into a readable product string."""
    if not exponents:
        return "1"

    parts = []
    for prime_value in sorted(exponents):
        exponent = exponents[prime_value]
        if exponent == 1:
            parts.append(str(prime_value))
        else:
            parts.append(f"{prime_value}^{exponent}")
    return " * ".join(parts)


def has_repeated_factors(exponents):
    """Return True when any factor in the witness product has exponent > 1."""
    return any(exponent > 1 for exponent in exponents.values())


def _generate_products(current_primes, limit, allow_repeated_factors):
    products = {}

    def generate(product, exponents, index):
        if product >= limit:
            return
        products[product] = exponents.copy()

        for i in range(index, len(current_primes)):
            prime_value = current_primes[i]
            if not allow_repeated_factors and prime_value in exponents:
                continue

            next_index = i if allow_repeated_factors else i + 1
            next_product = product * prime_value
            if next_product < limit:
                new_exponents = exponents.copy()
                new_exponents[prime_value] = new_exponents.get(prime_value, 0) + 1
                generate(next_product, new_exponents, next_index)

    generate(1, {}, 0)
    return products


def get_candidates(
    current_primes,
    limit,
    allow_repeated_factors=True,
    factor_composites=True,
):
    """Return Euclid-style candidate witness values from the current prime set."""
    products = _generate_products(current_primes, limit, allow_repeated_factors)
    candidates = []

    for product, exponents in products.items():
        result = product + 1
        if result >= limit:
            continue

        if is_prime(result):
            new_primes = []
            if result not in current_primes:
                new_primes.append(result)
            candidates.append(
                {
                    "product": product,
                    "exponents": exponents,
                    "result": result,
                    "result_is_prime": True,
                    "factors": [result],
                    "new_primes": sorted(new_primes),
                    "discovery_kind": "direct",
                    "used_repeated_factors": has_repeated_factors(exponents),
                }
            )
            continue

        if factor_composites:
            factors = sorted(set(prime_factors(result)))
            new_primes = [factor for factor in factors if factor not in current_primes]
            if new_primes:
                candidates.append(
                    {
                        "product": product,
                        "exponents": exponents,
                        "result": result,
                        "result_is_prime": False,
                        "factors": factors,
                        "new_primes": new_primes,
                        "discovery_kind": "factorization",
                        "used_repeated_factors": has_repeated_factors(exponents),
                    }
                )

    return sorted(candidates, key=lambda item: (item["result"], item["new_primes"]))


def _build_summary(results):
    reference_primes = results["reference_primes"]
    experiment_primes = results["experiment_primes"]
    discovered = results["discovered"]
    direct_count = sum(1 for item in discovered if item["discovery_kind"] == "direct")
    factorization_count = sum(
        1 for item in discovered if item["discovery_kind"] == "factorization"
    )
    coverage = 0.0
    if reference_primes:
        coverage = (len(experiment_primes) / len(reference_primes)) * 100

    return {
        "reference_prime_count": len(reference_primes),
        "experiment_prime_count": len(experiment_primes),
        "missing_prime_count": len(results["missing_primes"]),
        "coverage_percent": round(coverage, 2),
        "direct_discovery_count": direct_count,
        "factorization_discovery_count": factorization_count,
        "iteration_count": len(results["iterations"]),
    }


def run_euclid_experiment(
    seed_primes,
    limit,
    allow_repeated_factors=True,
    factor_composites=True,
    mode_name=None,
):
    """Run a Euclid-style experiment and return structured results."""
    seed_primes = sorted(set(seed_primes))
    known_primes = seed_primes[:]
    discovery_counter = 0
    discovered = []

    for prime_value in seed_primes:
        discovery_counter += 1
        discovered.append(
            {
                "prime": prime_value,
                "discovery_index": discovery_counter,
                "iteration": 0,
                "source_product": prime_value - 1,
                "source_result": prime_value,
                "exponents": {prime_value: 1},
                "combination": format_combination({prime_value: 1}),
                "result_is_prime": True,
                "factors": [prime_value],
                "discovery_kind": "seed",
                "used_repeated_factors": False,
            }
        )

    iterations = []

    while True:
        candidates = get_candidates(
            known_primes,
            limit,
            allow_repeated_factors=allow_repeated_factors,
            factor_composites=factor_composites,
        )
        if not candidates:
            break

        new_this_round = []
        iteration_number = len(iterations) + 1
        for candidate in candidates:
            added_primes = []
            for prime_value in candidate["new_primes"]:
                if prime_value in known_primes:
                    continue

                known_primes.append(prime_value)
                discovery_counter += 1
                discovery_entry = {
                    "prime": prime_value,
                    "discovery_index": discovery_counter,
                    "iteration": iteration_number,
                    "source_product": candidate["product"],
                    "source_result": candidate["result"],
                    "exponents": candidate["exponents"],
                    "combination": format_combination(candidate["exponents"]),
                    "result_is_prime": candidate["result_is_prime"],
                    "factors": candidate["factors"],
                    "discovery_kind": candidate["discovery_kind"],
                    "used_repeated_factors": candidate["used_repeated_factors"],
                }
                discovered.append(discovery_entry)
                added_primes.append(prime_value)

            if added_primes:
                round_entry = candidate.copy()
                round_entry["iteration"] = iteration_number
                round_entry["combination"] = format_combination(candidate["exponents"])
                round_entry["new_primes"] = added_primes
                new_this_round.append(round_entry)

        if not new_this_round:
            break
        iterations.append(new_this_round)

    reference_primes = all_primes_below(limit)
    experiment_primes = sorted(set(known_primes))
    missing_primes = [
        prime_value for prime_value in reference_primes if prime_value not in experiment_primes
    ]

    results = {
        "mode": mode_name,
        "settings": {
            "seed_primes": seed_primes,
            "limit": limit,
            "allow_repeated_factors": allow_repeated_factors,
            "factor_composites": factor_composites,
        },
        "reference_primes": reference_primes,
        "experiment_primes": experiment_primes,
        "missing_primes": missing_primes,
        "iterations": iterations,
        "discovered": discovered,
    }
    results["summary"] = _build_summary(results)
    return results


def run_named_mode(mode_name, seed_primes, limit):
    """Run one of the named experiment modes."""
    config = get_mode_config(mode_name)
    return run_euclid_experiment(
        seed_primes=seed_primes,
        limit=limit,
        allow_repeated_factors=config["allow_repeated_factors"],
        factor_composites=config["factor_composites"],
        mode_name=mode_name,
    )


def mode_label(results):
    """Return a readable label for an experiment configuration."""
    repeat_label = (
        "repeated factors allowed"
        if results["settings"]["allow_repeated_factors"]
        else "square-free only"
    )
    factor_label = (
        "factor composite results"
        if results["settings"]["factor_composites"]
        else "prime results only"
    )
    return f"{repeat_label}; {factor_label}"
