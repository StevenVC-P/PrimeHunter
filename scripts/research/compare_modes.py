import argparse
import json
from pathlib import Path

from primehunter.analysis.euclid import DEFAULT_LIMIT, DEFAULT_SEED, MODE_CONFIGS, parse_seed, run_named_mode

DEFAULT_TEXT_OUTPUT = "outputs/comparisons/mode_comparison.txt"
DEFAULT_JSON_OUTPUT = "outputs/comparisons/mode_comparison.json"


def _prepare_output_path(output_path):
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def build_mode_summary(results, preview_count):
    summary = results["summary"]
    return {
        "mode": results["mode"],
        "mode_label": results["mode"],
        "description": MODE_CONFIGS[results["mode"]]["description"],
        "found_count": summary["experiment_prime_count"],
        "missing_count": summary["missing_prime_count"],
        "coverage_percent": summary["coverage_percent"],
        "direct_discovery_count": summary["direct_discovery_count"],
        "factorization_discovery_count": summary["factorization_discovery_count"],
        "first_discovered_primes": results["experiment_primes"][:preview_count],
        "first_missing_primes": results["missing_primes"][:preview_count],
    }


def parse_args():
    parser = argparse.ArgumentParser(description="Compare Primehunter experiment modes side by side.")
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
        "--modes",
        default=",".join(sorted(MODE_CONFIGS)),
        help="Comma-separated mode names to compare.",
    )
    parser.add_argument(
        "--preview-count",
        type=int,
        default=10,
        help="How many discovered or missing primes to preview in the summary.",
    )
    parser.add_argument(
        "--format",
        choices=["text", "json", "all"],
        default="text",
        help="Summary output format.",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Optional output path. For --format all, this is treated as a base filename stem.",
    )
    return parser.parse_args()


def parse_modes(modes_text):
    modes = []
    for part in modes_text.split(","):
        mode = part.strip()
        if not mode:
            continue
        if mode not in MODE_CONFIGS:
            known = ", ".join(sorted(MODE_CONFIGS))
            raise ValueError(f"Unknown mode '{mode}'. Expected one of: {known}")
        modes.append(mode)
    if not modes:
        raise ValueError("At least one mode must be provided.")
    return modes


def build_comparison(seed_primes, limit, modes, preview_count):
    mode_runs = []
    for mode in modes:
        results = run_named_mode(mode, seed_primes, limit)
        mode_runs.append(build_mode_summary(results, preview_count))

    return {
        "seed_primes": seed_primes,
        "limit": limit,
        "modes": mode_runs,
    }


def comparison_text(comparison):
    lines = [
        "Primehunter Mode Comparison",
        f"Seed primes: {comparison['seed_primes']}",
        f"Limit: {comparison['limit']}",
    ]

    for mode_summary in comparison["modes"]:
        lines.append("")
        lines.append(f"Mode: {mode_summary['mode']}")
        lines.append(f"Description: {mode_summary['description']}")
        lines.append(
            "Coverage: "
            f"{mode_summary['found_count']} found, "
            f"{mode_summary['missing_count']} missing, "
            f"{mode_summary['coverage_percent']}%"
        )
        lines.append(
            "Discovery kinds: "
            f"direct={mode_summary['direct_discovery_count']}, "
            f"factorization={mode_summary['factorization_discovery_count']}"
        )
        lines.append(f"First discovered primes: {mode_summary['first_discovered_primes']}")
        lines.append(f"First missing primes: {mode_summary['first_missing_primes']}")

    return "\n".join(lines) + "\n"


def write_comparison_outputs(comparison, output_format, output_path=None):
    if output_format == "json":
        path = _prepare_output_path(output_path or DEFAULT_JSON_OUTPUT)
        with open(path, "w", encoding="utf-8") as output_file:
            json.dump(comparison, output_file, indent=2)
        return

    if output_format == "text":
        path = _prepare_output_path(output_path or DEFAULT_TEXT_OUTPUT)
        with open(path, "w", encoding="utf-8") as output_file:
            output_file.write(comparison_text(comparison))
        return

    if output_format == "all":
        if output_path:
            base = Path(output_path)
            stem = base.with_suffix("")
            text_path = f"{stem}.txt"
            json_path = f"{stem}.json"
        else:
            text_path = DEFAULT_TEXT_OUTPUT
            json_path = DEFAULT_JSON_OUTPUT

        write_comparison_outputs(comparison, "text", text_path)
        write_comparison_outputs(comparison, "json", json_path)
        return

    raise ValueError(f"Unsupported format '{output_format}'.")


def main():
    args = parse_args()
    seed_primes = parse_seed(args.seed, DEFAULT_SEED)
    modes = parse_modes(args.modes)
    comparison = build_comparison(seed_primes, args.limit, modes, args.preview_count)
    write_comparison_outputs(comparison, args.format, args.output)


if __name__ == "__main__":
    main()
