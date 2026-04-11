# Residue View Tool

## Purpose

This tool is a derived PrimeHunter v1 tool built on canonical center-analysis records.

It provides a basic small-prime residue view for each center against a fixed default tracked-prime set of `5,7,11`.
It is meant to support simple residue and elimination inspection without replacing the factor-based canonical record model.
It is not a wheel system, not a generalized sieve engine, and not a modular-analysis framework.

## Main Files

- `primehunter/tools/residue_view/`
  Tool package.

- `scripts/tools/residue_view_experiment.py`
  Local runner for generating test output.

## Status

- built: yes
- tested: partial
- deployed: internal-only

## How To Run

Default run:

```powershell
python -m scripts.tools.residue_view_experiment
```

Run a smaller range:

```powershell
python -m scripts.tools.residue_view_experiment --start-n 1 --end-n 20
```

Inspect a small custom tracked-prime list:

```powershell
python -m scripts.tools.residue_view_experiment --start-n 1 --end-n 20 --primes 5,7,13
```

Run in summary-only mode:

```powershell
python -m scripts.tools.residue_view_experiment --start-n 1 --end-n 1000000 --summary-only
```

## Output

Default output files:

- full-record mode: `outputs/residue_view/residue_view.json`
- summary-only mode: `outputs/residue_view/residue_view_summary.json`

The tool writes structured JSON only.
Text printed to the terminal is summary-only.

## Current Limits

- local/internal use only
- no API surface yet
- v1 remains fixed to the `6n` center framework
- wheel is fixed to `6`
- analysis is currently range-based by `n`
- full-record mode hard limit: `100000` centers
- summary-only mode hard limit: `1000000` centers
- default tracked primes are `5,7,11`
- custom tracked primes are allowed only as a small bounded inspection input
- tracked-prime lists are limited to `6` values in v1
- tracked primes must be unique prime integers greater than `3`
- this tool is derived from center-analysis records and does not replace the center-analysis foundation
- allowing custom tracked primes does not make this tool a generic wheel implementation

## Current Success Condition

This tool is considered successful at the current stage when it:

- runs locally
- writes valid structured JSON
- reports residue values for both sides
- identifies simple small-prime elimination on composite sides only
- summarizes left/right eliminations by tracked prime


