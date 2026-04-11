"""Classification helpers for twin-prime centers."""

TWIN_PRIME = "twin_prime"
LEFT_ONLY_PRIME = "left_only_prime"
RIGHT_ONLY_PRIME = "right_only_prime"
NEITHER_PRIME = "neither_prime"

CLASSIFICATIONS = (
    TWIN_PRIME,
    LEFT_ONLY_PRIME,
    RIGHT_ONLY_PRIME,
    NEITHER_PRIME,
)


def classify_center(left_is_prime, right_is_prime):
    """Return the canonical center classification."""
    if left_is_prime and right_is_prime:
        return TWIN_PRIME
    if left_is_prime:
        return LEFT_ONLY_PRIME
    if right_is_prime:
        return RIGHT_ONLY_PRIME
    return NEITHER_PRIME


def is_twin_prime_class(classification):
    """Return True when the classification represents a twin prime center."""
    return classification == TWIN_PRIME
