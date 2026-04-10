import argparse

from primehunter.analysis.euclid import DEFAULT_LIMIT, DEFAULT_SEED, MODE_CONFIGS, parse_seed, run_named_mode
from primehunter.data.euclid_exports import write_multiple_formats


def parse_args():
    parser = argparse.ArgumentParser(description="Run a Primehunter Euclid-style experiment.")
    parser.add_argument(
        "--mode",
        choices=sorted(MODE_CONFIGS),
        default="full",
        help="Experiment mode to run.",
    )
    parser.add_argument(
        "--seed",
        default=",".join(str(value) for value in DEFAULT_SEED),
        help="Comma-separated seed primes, for example 2 or 2,3.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=DEFAULT_LIMIT,
        help="Upper bound (exclusive) for discoveries and reference comparison.",
    )
    parser.add_argument(
        "--format",
        choices=["text", "json", "csv", "all"],
        default="text",
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
    seed_primes = parse_seed(args.seed, DEFAULT_SEED)
    results = run_named_mode(args.mode, seed_primes, args.limit)
    formats = ["text", "json", "csv"] if args.format == "all" else [args.format]
    write_multiple_formats(results, args.mode, formats, args.output)


if __name__ == "__main__":
    main()
