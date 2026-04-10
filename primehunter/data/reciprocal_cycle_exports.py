"""Writers for reciprocal-cycle experiment outputs."""

from __future__ import annotations

import csv
import json
from pathlib import Path

FORMAT_SUFFIXES = {
    "text": "txt",
    "json": "json",
    "csv": "csv",
}


def _prepare_output_path(output_path):
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def summary_text(results):
    """Return a short terminal summary for the reciprocal-cycle experiment."""
    summary = results["summary"]
    counts = summary["maximal_order_counts"]
    overall_counts = ", ".join(
        f"base {base} = {counts[f'base{base}_overall']}" for base in results["bases"]
    )
    twin_counts = ", ".join(
        f"base {base} = {counts[f'base{base}_twin_primes']}" for base in results["bases"]
    )

    lines = [
        "Primehunter Reciprocal Cycle Experiment",
        f"Bases: {results['bases']}",
        f"Limit: {summary['limit']}",
        (
            f"Analyzed {summary['analyzed_prime_count']} primes "
            f"(skipped {summary['skipped_primes']})."
        ),
        f"Twin primes in range: {summary['twin_prime_count']}",
        f"Maximal order counts overall: {overall_counts}",
        f"Maximal order counts among twin primes: {twin_counts}",
    ]
    return "\n".join(lines)


def write_text_report(output_path, results):
    """Write a human-readable text report."""
    output_path = _prepare_output_path(output_path)
    with open(output_path, "w", encoding="utf-8") as output_file:
        output_file.write(summary_text(results))
        output_file.write("\n\nPer-prime results:\n")
        for record in results["primes"]:
            base_parts = []
            for base in results["bases"]:
                base_parts.append(
                    (
                        f"ord_{{p}}({base})={record[f'base{base}_order']} "
                        f"({record[f'base{base}_ratio']:.4f})"
                    )
                )
            output_file.write(
                f"p={record['prime']}: {', '.join(base_parts)}, twin={record['is_twin_prime']}\n"
            )
            if results["summary"]["include_expansions"]:
                for base in results["bases"]:
                    output_file.write(
                        f"  1/p in base {base}: {record[f'base{base}_expansion']}\n"
                    )


def write_json(output_path, results):
    """Write a JSON export."""
    output_path = _prepare_output_path(output_path)
    with open(output_path, "w", encoding="utf-8") as output_file:
        json.dump(results, output_file, indent=2)


def write_csv(output_path, results):
    """Write a flat CSV export."""
    output_path = _prepare_output_path(output_path)
    fieldnames = ["prime"]
    for base in results["bases"]:
        fieldnames.extend([f"base{base}_order", f"base{base}_ratio"])
    fieldnames.extend(["has_twin_lower", "has_twin_upper", "is_twin_prime"])

    include_expansions = results["summary"]["include_expansions"]
    if include_expansions:
        for base in results["bases"]:
            fieldnames.extend([f"base{base}_expansion", f"base{base}_repeating"])

    with open(output_path, "w", newline="", encoding="utf-8") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader()
        for record in results["primes"]:
            writer.writerow({field: record.get(field, "") for field in fieldnames})


def write_results(output_path, results, output_format):
    """Write results in the requested format."""
    if output_format == "text":
        write_text_report(output_path, results)
        return
    if output_format == "json":
        write_json(output_path, results)
        return
    if output_format == "csv":
        write_csv(output_path, results)
        return
    raise ValueError(f"Unsupported output format '{output_format}'.")


def default_output_path(output_format):
    """Return the default output path for the reciprocal-cycle experiment."""
    filename_map = {
        "text": "outputs/reciprocal_cycles/reciprocal_cycles_output.txt",
        "json": "outputs/reciprocal_cycles/reciprocal_cycles_output.json",
        "csv": "outputs/reciprocal_cycles/reciprocal_cycles_output.csv",
    }
    return filename_map[output_format]


def write_multiple_formats(results, formats, output_path=None):
    """Write the reciprocal-cycle results in one or more formats."""
    normalized_formats = list(formats)
    if output_path and len(normalized_formats) > 1:
        base = Path(output_path)
        stem = base.with_suffix("")
        for output_format in normalized_formats:
            suffix = FORMAT_SUFFIXES[output_format]
            write_results(f"{stem}.{suffix}", results, output_format)
        return

    for output_format in normalized_formats:
        path = output_path or default_output_path(output_format)
        write_results(path, results, output_format)
