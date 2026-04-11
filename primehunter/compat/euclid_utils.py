"""Compatibility wrapper for Euclid-style PrimeHunter helpers."""

from primehunter.analysis.euclid import (
    DEFAULT_LIMIT,
    DEFAULT_SEED,
    MODE_CONFIGS,
    format_combination,
    get_candidates,
    get_mode_config,
    has_repeated_factors,
    mode_label,
    parse_seed,
    run_euclid_experiment,
    run_named_mode,
)
from primehunter.data.euclid_exports import (
    default_output_path,
    json_ready_results,
    write_discovery_csv,
    write_experiment_json,
    write_experiment_report,
    write_multiple_formats,
    write_results,
)

__all__ = [
    "DEFAULT_LIMIT",
    "DEFAULT_SEED",
    "MODE_CONFIGS",
    "default_output_path",
    "format_combination",
    "get_candidates",
    "get_mode_config",
    "has_repeated_factors",
    "json_ready_results",
    "mode_label",
    "parse_seed",
    "run_euclid_experiment",
    "run_named_mode",
    "write_discovery_csv",
    "write_experiment_json",
    "write_experiment_report",
    "write_multiple_formats",
    "write_results",
]
