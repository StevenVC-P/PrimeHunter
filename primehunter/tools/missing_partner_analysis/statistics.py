"""Summary helpers for missing-partner analysis."""


def build_summary_from_counts(analyzed_center_count, left_count, right_count, frequencies):
    """Build a canonical summary block from aggregate counts."""
    missing_partner_count = left_count + right_count
    if missing_partner_count == 0:
        left_ratio = 0.0
        right_ratio = 0.0
    else:
        left_ratio = round(left_count / missing_partner_count, 6)
        right_ratio = round(right_count / missing_partner_count, 6)

    return {
        "center_count": analyzed_center_count,
        "missing_partner_count": missing_partner_count,
        "left_missing_partner_count": left_count,
        "right_missing_partner_count": right_count,
        "left_missing_partner_ratio": left_ratio,
        "right_missing_partner_ratio": right_ratio,
        "smallest_disruptor_frequencies": frequencies,
    }


def build_summary(records, analyzed_center_count=None):
    """Build a summary block for missing-partner records."""
    frequencies = {}
    left_count = 0
    right_count = 0

    for record in records:
        if record["classification"] == "left_only_prime":
            left_count += 1
            disruptor = record["right"]["smallest_disruptor"]
        else:
            right_count += 1
            disruptor = record["left"]["smallest_disruptor"]

        key = str(disruptor)
        frequencies[key] = frequencies.get(key, 0) + 1

    if analyzed_center_count is None:
        analyzed_center_count = len(records)

    return build_summary_from_counts(
        analyzed_center_count=analyzed_center_count,
        left_count=left_count,
        right_count=right_count,
        frequencies=frequencies,
    )
