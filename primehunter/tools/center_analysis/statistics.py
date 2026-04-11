"""Summary statistics for canonical center records."""

from primehunter.tools.center_analysis.classification import (
    LEFT_ONLY_PRIME,
    NEITHER_PRIME,
    RIGHT_ONLY_PRIME,
    TWIN_PRIME,
)


def build_empty_summary():
    """Return an empty mutable summary accumulator."""
    return {
        "center_count": 0,
        "twin_prime_count": 0,
        "left_only_prime_count": 0,
        "right_only_prime_count": 0,
        "neither_prime_count": 0,
        "smallest_disruptor_frequencies": {},
    }


def update_summary(summary, record):
    """Update a mutable summary accumulator with one center record."""
    summary["center_count"] += 1

    classification = record["classification"]
    if classification == TWIN_PRIME:
        summary["twin_prime_count"] += 1
    elif classification == LEFT_ONLY_PRIME:
        summary["left_only_prime_count"] += 1
    elif classification == RIGHT_ONLY_PRIME:
        summary["right_only_prime_count"] += 1
    elif classification == NEITHER_PRIME:
        summary["neither_prime_count"] += 1

    for side_name in ("left", "right"):
        disruptor = record[side_name]["smallest_disruptor"]
        if disruptor is None:
            continue
        key = str(disruptor)
        summary["smallest_disruptor_frequencies"][key] = (
            summary["smallest_disruptor_frequencies"].get(key, 0) + 1
        )

    return summary


def finalize_summary(summary):
    """Finalize density metrics for a completed summary accumulator."""
    if summary["center_count"] == 0:
        twin_ratio = 0.0
    else:
        twin_ratio = round(summary["twin_prime_count"] / summary["center_count"], 6)
    summary["twin_prime_ratio"] = twin_ratio
    return summary


def summarize_classifications(records):
    """Count canonical classifications across records."""
    return {
        "center_count": len(records),
        "twin_prime_count": sum(1 for record in records if record["classification"] == TWIN_PRIME),
        "left_only_prime_count": sum(
            1 for record in records if record["classification"] == LEFT_ONLY_PRIME
        ),
        "right_only_prime_count": sum(
            1 for record in records if record["classification"] == RIGHT_ONLY_PRIME
        ),
        "neither_prime_count": sum(
            1 for record in records if record["classification"] == NEITHER_PRIME
        ),
    }


def summarize_disruptors(records):
    """Count smallest disruptor frequencies across composite sides."""
    frequencies = {}
    for record in records:
        for side_name in ("left", "right"):
            disruptor = record[side_name]["smallest_disruptor"]
            if disruptor is None:
                continue
            key = str(disruptor)
            frequencies[key] = frequencies.get(key, 0) + 1
    return {"smallest_disruptor_frequencies": frequencies}


def summarize_density(records):
    """Return simple density and survival ratios."""
    center_count = len(records)
    twin_prime_count = sum(1 for record in records if record["classification"] == TWIN_PRIME)
    if center_count == 0:
        twin_ratio = 0.0
    else:
        twin_ratio = round(twin_prime_count / center_count, 6)
    return {"twin_prime_ratio": twin_ratio}


def build_summary(records):
    """Return the canonical summary block."""
    summary = {}
    summary.update(summarize_classifications(records))
    summary.update(summarize_disruptors(records))
    summary.update(summarize_density(records))
    return summary
