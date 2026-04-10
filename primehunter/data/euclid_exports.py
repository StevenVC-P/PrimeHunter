"""Writers for Euclid-style experiment outputs."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from primehunter.analysis.euclid import mode_label


def _prepare_output_path(output_path):
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def write_experiment_report(output_path, results):
    """Write the traditional text report for a single experiment run."""
    summary = results["summary"]
    output_path = _prepare_output_path(output_path)

    with open(output_path, "w", encoding="utf-8") as output_file:
        print("Euclid-style prime exploration", file=output_file)
        if results["mode"]:
            print(f"Mode name: {results['mode']}", file=output_file)
        print(f"Mode: {mode_label(results)}", file=output_file)
        print(f"Seed primes: {results['settings']['seed_primes']}", file=output_file)
        print(f"Limit: {results['settings']['limit']}", file=output_file)

        for iteration_number, found_in_iteration in enumerate(results["iterations"], 1):
            print(f"\nIteration {iteration_number}:", file=output_file)
            for entry in found_in_iteration:
                new_primes_str = ", ".join(str(prime_value) for prime_value in entry["new_primes"])
                if entry["result_is_prime"]:
                    print(
                        (
                            f"Found {new_primes_str} from ({entry['combination']}) + 1 = "
                            f"{entry['result']}"
                        ),
                        file=output_file,
                    )
                else:
                    factors_str = " * ".join(str(factor) for factor in entry["factors"])
                    print(
                        (
                            f"Found {new_primes_str} from ({entry['combination']}) + 1 = "
                            f"{entry['result']} = {factors_str}"
                        ),
                        file=output_file,
                    )

        print("\nSummary", file=output_file)
        print(
            (
                f"Found {summary['experiment_prime_count']} of the "
                f"{summary['reference_prime_count']} reference primes below "
                f"{results['settings']['limit']}."
            ),
            file=output_file,
        )
        print(
            f"Missing {summary['missing_prime_count']} reference primes below "
            f"{results['settings']['limit']}.",
            file=output_file,
        )
        print(f"Coverage: {summary['coverage_percent']}%", file=output_file)
        print(
            (
                "Discovery kinds: "
                f"direct={summary['direct_discovery_count']}, "
                f"factorization={summary['factorization_discovery_count']}"
            ),
            file=output_file,
        )

        print(f"\nExperiment primes below {results['settings']['limit']}:", file=output_file)
        print(results["experiment_primes"], file=output_file)

        print(f"\nReference primes below {results['settings']['limit']}:", file=output_file)
        print(results["reference_primes"], file=output_file)

        print(f"\nMissing reference primes below {results['settings']['limit']}:", file=output_file)
        print(results["missing_primes"], file=output_file)

        print("\nOrder of discovery:", file=output_file)
        for discovery in results["discovered"]:
            if discovery["discovery_kind"] == "seed":
                print(
                    f"n{discovery['discovery_index']} = {discovery['prime']}  (seed prime)",
                    file=output_file,
                )
                continue

            suffix = f"{discovery['source_result']}"
            if not discovery["result_is_prime"]:
                factors_str = " * ".join(str(factor) for factor in discovery["factors"])
                suffix = f"{discovery['source_result']} = {factors_str}"
            print(
                (
                    f"n{discovery['discovery_index']} = {discovery['prime']}  "
                    f"(from {discovery['combination']} + 1 = {suffix}; "
                    f"{discovery['discovery_kind']})"
                ),
                file=output_file,
            )


def json_ready_results(results):
    """Return a JSON-serializable export shape for Euclid experiments."""
    return {
        "mode": results["mode"],
        "mode_label": mode_label(results),
        "settings": results["settings"],
        "summary": results["summary"],
        "reference_primes": results["reference_primes"],
        "experiment_primes": results["experiment_primes"],
        "missing_primes": results["missing_primes"],
        "iterations": results["iterations"],
        "discovered": results["discovered"],
    }


def write_experiment_json(output_path, results):
    """Write a JSON export for a single experiment run."""
    output_path = _prepare_output_path(output_path)
    with open(output_path, "w", encoding="utf-8") as output_file:
        json.dump(json_ready_results(results), output_file, indent=2)


def write_discovery_csv(output_path, results):
    """Write a flat CSV discovery log for a single experiment run."""
    output_path = _prepare_output_path(output_path)
    fieldnames = [
        "discovery_index",
        "iteration",
        "prime",
        "discovery_kind",
        "result_is_prime",
        "source_product",
        "source_result",
        "combination",
        "used_repeated_factors",
        "factors",
    ]

    with open(output_path, "w", newline="", encoding="utf-8") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader()
        for discovery in results["discovered"]:
            writer.writerow(
                {
                    "discovery_index": discovery["discovery_index"],
                    "iteration": discovery["iteration"],
                    "prime": discovery["prime"],
                    "discovery_kind": discovery["discovery_kind"],
                    "result_is_prime": discovery["result_is_prime"],
                    "source_product": discovery["source_product"],
                    "source_result": discovery["source_result"],
                    "combination": discovery["combination"],
                    "used_repeated_factors": discovery["used_repeated_factors"],
                    "factors": ",".join(str(factor) for factor in discovery["factors"]),
                }
            )


def write_results(output_path, results, output_format="text"):
    """Write one experiment result in text, JSON, or CSV form."""
    if output_format == "text":
        write_experiment_report(output_path, results)
        return
    if output_format == "json":
        write_experiment_json(output_path, results)
        return
    if output_format == "csv":
        write_discovery_csv(output_path, results)
        return
    raise ValueError(f"Unsupported output format '{output_format}'.")


def default_output_path(mode_name, output_format):
    """Return the default output path for a named mode and format."""
    filename_map = {
        ("full", "text"): "outputs/euclid/primes_output.txt",
        ("full", "json"): "outputs/euclid/primes_output.json",
        ("full", "csv"): "outputs/euclid/primes_output.csv",
        ("square_free_factor", "text"): "outputs/euclid/primes_square_free_output.txt",
        ("square_free_factor", "json"): "outputs/euclid/primes_square_free_output.json",
        ("square_free_factor", "csv"): "outputs/euclid/primes_square_free_output.csv",
        ("square_free_no_factor", "text"): "outputs/euclid/primes_square_free_no_factor_output.txt",
        ("square_free_no_factor", "json"): "outputs/euclid/primes_square_free_no_factor_output.json",
        ("square_free_no_factor", "csv"): "outputs/euclid/primes_square_free_no_factor_output.csv",
    }
    return filename_map[(mode_name, output_format)]


def write_multiple_formats(results, mode_name, formats, output_path=None):
    """Write one result in one or more formats."""
    normalized_formats = list(formats)
    if output_path and len(normalized_formats) > 1:
        base = Path(output_path)
        stem = base.with_suffix("")
        for output_format in normalized_formats:
            write_results(f"{stem}.{output_format}", results, output_format)
        return

    for output_format in normalized_formats:
        path = output_path or default_output_path(mode_name, output_format)
        write_results(path, results, output_format)
