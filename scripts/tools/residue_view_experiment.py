import argparse
from datetime import datetime, timezone
from pathlib import Path

from primehunter.tools.residue_view import (
    analyze_residue_view_range,
    build_result_envelope,
    build_summary,
    write_json_output,
)
from primehunter.tools.residue_view.tool import (
    DEFAULT_RESIDUE_PRIMES,
    MAX_TRACKED_PRIMES,
    normalize_tracked_primes,
)

DEFAULT_OUTPUT = "outputs/residue_view/residue_view.json"
DEFAULT_SUMMARY_OUTPUT = "outputs/residue_view/residue_view_summary.json"
MAX_RECORD_CENTERS = 100000
MAX_SUMMARY_CENTERS = 1000000


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run residue-view analysis for an inclusive range of center n values."
    )
    parser.add_argument("--start-n", type=int, default=1, help="First n value to analyze.")
    parser.add_argument("--end-n", type=int, default=100, help="Last n value to analyze.")
    parser.add_argument(
        "--primes",
        default=",".join(str(value) for value in DEFAULT_RESIDUE_PRIMES),
        help=(
            "Comma-separated tracked primes for the residue view. "
            f"Defaults to {','.join(str(value) for value in DEFAULT_RESIDUE_PRIMES)} and is limited "
            f"to {MAX_TRACKED_PRIMES} small inspection primes in v1."
        ),
    )
    parser.add_argument(
        "--summary-only",
        action="store_true",
        help="Write only summary data and omit per-record residue-view records.",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Path for the JSON output. Defaults depend on whether --summary-only is used.",
    )
    return parser.parse_args()


def parse_primes(primes_text):
    values = []
    for part in primes_text.split(","):
        text = part.strip()
        if not text:
            continue
        values.append(int(text))
    return normalize_tracked_primes(values)


def default_output_path(summary_only):
    return DEFAULT_SUMMARY_OUTPUT if summary_only else DEFAULT_OUTPUT


def validate_range(start_n, end_n, summary_only):
    center_count = end_n - start_n + 1
    if center_count < 1:
        raise ValueError("end-n must be greater than or equal to start-n.")
    max_centers = MAX_SUMMARY_CENTERS if summary_only else MAX_RECORD_CENTERS
    if center_count > max_centers:
        mode_label = "summary-only" if summary_only else "full-record"
        raise ValueError(
            f"Requested {center_count} centers, but the {mode_label} limit is {max_centers}."
        )
    return center_count


def build_metadata(start_n, end_n, center_count, summary_only, residue_primes):
    mode = "summary_only" if summary_only else "full_record"
    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "mode": mode,
        "record_limit": MAX_RECORD_CENTERS,
        "summary_limit": MAX_SUMMARY_CENTERS,
        "tracked_prime_limit": MAX_TRACKED_PRIMES,
        "requested_start_n": start_n,
        "requested_end_n": end_n,
        "center_count": center_count,
        "tracked_primes": residue_primes,
    }


def main():
    args = parse_args()
    residue_primes = parse_primes(args.primes)
    center_count = validate_range(args.start_n, args.end_n, args.summary_only)
    output_path = args.output or default_output_path(args.summary_only)

    all_records = analyze_residue_view_range(args.start_n, args.end_n, primes=residue_primes)
    summary = build_summary(all_records, residue_primes)
    records = [] if args.summary_only else all_records

    payload = build_result_envelope(
        experiment="residue_view",
        input_data={
            "start_n": args.start_n,
            "end_n": args.end_n,
            "wheel": 6,
            "summary_only": args.summary_only,
            "center_count": center_count,
            "tracked_primes": residue_primes,
        },
        summary=summary,
        records=records,
        metadata=build_metadata(args.start_n, args.end_n, center_count, args.summary_only, residue_primes),
    )
    write_json_output(output_path, payload)
    print(f"Analyzed {center_count} centers with residue primes {residue_primes}.")
    print(f"Wrote output to {Path(output_path)}")


if __name__ == "__main__":
    main()
