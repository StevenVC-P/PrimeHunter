"""Canonical JSON outputs for PrimeHunter v1 missing-partner analysis tool."""

from __future__ import annotations

import json
from pathlib import Path


def build_result_envelope(experiment, input_data, summary, records, metadata=None):
    """Return the canonical JSON-ready result envelope."""
    payload = {
        "experiment": experiment,
        "version": "v1",
        "input": input_data,
        "summary": summary,
        "records": records,
    }
    if metadata is not None:
        payload["metadata"] = metadata
    return payload


def write_json_output(path, payload):
    """Write a canonical JSON payload to disk."""
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as output_file:
        json.dump(payload, output_file, indent=2)
