from pathlib import Path

from primehunter.math_core.primes import all_primes_below

DEFAULT_OUTPUT = "outputs/reference/primes_master_10000.txt"


def write_master_prime_list(limit, output_path):
    """Write the canonical reference prime list below limit to a text file."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    primes = all_primes_below(limit)
    with open(output_path, "w", encoding="utf-8") as output_file:
        print(f"Master list of primes up to {limit:,}", file=output_file)
        print(f"Total primes: {len(primes)}", file=output_file)
        print(file=output_file)
        print(primes, file=output_file)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Write a reference list of primes below a limit.")
    parser.add_argument("--limit", type=int, default=10000, help="Upper bound (exclusive).")
    parser.add_argument(
        "--output",
        default=DEFAULT_OUTPUT,
        help="Path for the generated prime list.",
    )
    args = parser.parse_args()
    write_master_prime_list(args.limit, args.output)
