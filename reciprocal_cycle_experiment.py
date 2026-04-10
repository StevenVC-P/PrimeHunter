import argparse

from primehunter.analysis.reciprocal_cycles import (
    DEFAULT_BASES,
    DEFAULT_LIMIT,
    parse_bases,
    run_reciprocal_cycle_experiment,
)
from primehunter.data.reciprocal_cycle_exports import summary_text, write_multiple_formats


def parse_args():
    parser = argparse.ArgumentParser(
        description="Analyze reciprocal cycle structure of primes in bases 6 and 12."
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=DEFAULT_LIMIT,
        help="Upper bound (exclusive) for primes to analyze.",
    )
    parser.add_argument(
        "--bases",
        default=",".join(str(value) for value in DEFAULT_BASES),
        help="Comma-separated bases to analyze, for example 6,12 or 10.",
    )
    parser.add_argument(
        "--include-expansions",
        action="store_true",
        help="Include repeating expansions of 1/p in base 6 and base 12.",
    )
    parser.add_argument(
        "--format",
        choices=["text", "json", "csv", "all"],
        default="json",
        help="Output format to write.",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Optional output path. If --format all is used, this becomes the base filename stem.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    bases = parse_bases(args.bases)
    results = run_reciprocal_cycle_experiment(
        limit=args.limit,
        bases=bases,
        include_expansions=args.include_expansions,
    )
    print(summary_text(results))
    formats = ["text", "json", "csv"] if args.format == "all" else [args.format]
    write_multiple_formats(results, formats, args.output)


if __name__ == "__main__":
    main()
