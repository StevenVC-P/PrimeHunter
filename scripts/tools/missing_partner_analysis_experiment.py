import argparse
from datetime import datetime, timezone
from pathlib import Path

from primehunter.tools.missing_partner_analysis import (
    analyze_missing_partner_range,
    build_result_envelope,
    build_summary,
    summarize_missing_partner_range,
    write_json_output,
)

DEFAULT_OUTPUT = "outputs/missing_partner_analysis/missing_partner_analysis.json"
DEFAULT_SUMMARY_OUTPUT = "outputs/missing_partner_analysis/missing_partner_analysis_summary.json"
MAX_RECORD_CENTERS = 100000
MAX_SUMMARY_CENTERS = 1000000


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run missing-partner analysis for an inclusive range of center n values."
    )
    parser.add_argument("--start-n", type=int, default=1, help="First n value to analyze.")
    parser.add_argument("--end-n", type=int, default=100, help="Last n value to analyze.")
    parser.add_argument(
        "--summary-only",
        action="store_true",
        help="Write only summary data and omit per-record missing-partner cases.",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Path for the JSON output. Defaults depend on whether --summary-only is used.",
    )
    return parser.parse_args()


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


def build_metadata(start_n, end_n, center_count, summary_only):
    mode = "summary_only" if summary_only else "full_record"
    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "mode": mode,
        "record_limit": MAX_RECORD_CENTERS,
        "summary_limit": MAX_SUMMARY_CENTERS,
        "requested_start_n": start_n,
        "requested_end_n": end_n,
        "center_count": center_count,
    }


def main():
    args = parse_args()
    center_count = validate_range(args.start_n, args.end_n, args.summary_only)
    output_path = args.output or default_output_path(args.summary_only)

    if args.summary_only:
        records = []
        summary = summarize_missing_partner_range(args.start_n, args.end_n)
    else:
        records = analyze_missing_partner_range(args.start_n, args.end_n)
        summary = build_summary(records, analyzed_center_count=center_count)

    payload = build_result_envelope(
        experiment="missing_partner_analysis",
        input_data={
            "start_n": args.start_n,
            "end_n": args.end_n,
            "wheel": 6,
            "summary_only": args.summary_only,
            "center_count": center_count,
        },
        summary=summary,
        records=records,
        metadata=build_metadata(args.start_n, args.end_n, center_count, args.summary_only),
    )
    write_json_output(output_path, payload)
    print(
        f"Analyzed {center_count} centers; "
        f"found {summary['missing_partner_count']} missing-partner cases."
    )
    print(f"Wrote output to {Path(output_path)}")


if __name__ == "__main__":
    main()
