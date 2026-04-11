# Center Analysis Tool Review Guide

## Why This Tool Exists

This tool is the first implementation slice of the PrimeHunter v1 contract.

It exists to establish the canonical backend shape before broader experiment families are added.

The central idea is:

- the primary unit is the twin-prime center `6n`
- each record must include `left`, `right`, `classification`, and disruptor data
- outputs must be structured and JSON-first

## Canonical Scope

This tool currently covers:

- center generation
- left/right candidate construction
- primality evaluation
- classification
- smallest disruptor analysis
- full factorization for sides
- summary statistics
- JSON result-envelope writing
- summary-only local runs for larger ranges

It does not yet cover:

- residue-derived views
- sieve-layer views
- missing partner specialization as its own module
- APIs

## Package Layout

- `classification.py`
  Canonical four-state center classification.

- `disruptors.py`
  Smallest disruptor and full factorization logic.

- `records.py`
  Canonical side and center record construction.

- `statistics.py`
  Summary generation from record lists and summary-only accumulation.

- `tool.py`
  High-level center-analysis entry points.

- `json_outputs.py`
  Canonical JSON envelope and local JSON writing.

## Entry Point

Human/dev runner:

- `scripts/tools/center_analysis_experiment.py`

Current command examples:

```powershell
python -m scripts.tools.center_analysis_experiment
python -m scripts.tools.center_analysis_experiment --start-n 1 --end-n 12
python -m scripts.tools.center_analysis_experiment --start-n 1 --end-n 1000000 --summary-only
python -m scripts.tools.center_analysis_experiment --start-n 1 --end-n 100 --output outputs/center_analysis/twin_center_analysis.json
```

## Limits

Current enforced limits:

- full-record mode: `100000` centers
- summary-only mode: `1000000` centers

Current operational limits:

- fixed wheel scope of `6` only
- local file output only
- no public API
- test coverage is still minimal and focused
- no performance tuning for very large ranges beyond the hard limits
- no schema-version negotiation beyond the hardcoded `v1` envelope field
- CLI does not accept comma-formatted integer arguments

## Review Expectations For Agents

When reviewing or extending this tool, check:

- does the tool still treat `6n` as the canonical object
- are `left` and `right` always present in full-record mode
- does `classification` stay within the approved enum
- is `smallest_disruptor` `null` for prime sides
- does composite `factorization` remain structured and complete
- does JSON remain the canonical output
- are new derived features staying derived rather than replacing the center model
- do new range or output options preserve the hard-limit protections
- does metadata stay accurate and self-describing

## Extension Rule

Any future extension should answer:

- is this canonical or derived
- does it belong inside this tool or in a later tool
- does it preserve the v1 center-first contract
- does it still produce locally testable structured output


