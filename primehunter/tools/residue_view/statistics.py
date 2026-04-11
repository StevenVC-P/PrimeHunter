"""Summary helpers for residue-view analysis."""


def build_summary(records, residue_primes):
    """Build a summary block for residue-view records."""
    left_eliminations = {str(prime_value): 0 for prime_value in residue_primes}
    right_eliminations = {str(prime_value): 0 for prime_value in residue_primes}

    for record in records:
        for prime_value in record["left"]["eliminated_by"]:
            left_eliminations[str(prime_value)] += 1
        for prime_value in record["right"]["eliminated_by"]:
            right_eliminations[str(prime_value)] += 1

    return {
        "center_count": len(records),
        "tracked_primes": list(residue_primes),
        "left_elimination_counts": left_eliminations,
        "right_elimination_counts": right_eliminations,
    }
