# Residue View Tool Review Guide

## Why This Tool Exists

This tool is the third PrimeHunter v1 tool and a derived structural view built on the center-analysis foundation.

It exists to support basic small-prime residue elimination analysis while preserving the factor-based center-first model.

## Canonical Scope

This tool currently covers:

- per-side residues against the default v1 tracked-prime set `5,7,11`
- simple elimination flags for composite sides divisible by tracked primes
- per-prime elimination counts on the left and right sides
- local JSON result writing
- summary-only local runs for larger ranges
- small custom tracked-prime inputs for bounded local inspection

It does not yet cover:

- advanced residue overlap analysis
- wheel generalization
- sieve layering
- API access

## Package Layout

- `tool.py`
  Derived residue-view record generation and tracked-prime validation.

- `statistics.py`
  Summary generation for elimination counts.

- `json_outputs.py`
  Canonical JSON envelope and local JSON writing.

## Dependency Rule

This tool depends on canonical center-analysis records.

That dependency is intentional.
This tool should remain a derived view rather than a second foundational analysis engine.

## Entry Point

Human/dev runner:

- `scripts/tools/residue_view_experiment.py`

Current command examples:

```powershell
python -m scripts.tools.residue_view_experiment
python -m scripts.tools.residue_view_experiment --start-n 1 --end-n 20
python -m scripts.tools.residue_view_experiment --start-n 1 --end-n 20 --primes 5,7,13
python -m scripts.tools.residue_view_experiment --start-n 1 --end-n 1000000 --summary-only
```

## Limits

Current enforced limits:

- full-record mode: `100000` centers
- summary-only mode: `1000000` centers
- tracked-prime list limit: `6` values

Current operational limits:

- default tracked primes are `5,7,11`
- fixed wheel scope of `6` only
- fixed `6n` center framework only
- local file output only
- no public API
- test coverage is still minimal and focused
- tracked primes are small-prime inspection inputs, not a generic wheel engine
- allowing custom tracked primes does not imply generalized sieve-layer or wheel support

## Review Expectations For Agents

When reviewing or extending this tool, check:

- does it remain derived from center-analysis records
- does it keep `5,7,11` as the default tracked-prime set for v1
- does it report residues for both sides consistently
- does it only mark elimination for composite sides divisible by tracked primes
- does it avoid treating a prime equal to a tracked prime as an eliminated composite case
- does it keep custom tracked-prime inputs bounded and small
- do left/right elimination summaries match the record-level data
- do hard limits remain enforced
- does it avoid drifting into generic wheel-engine design

## Extension Rule

Any future extension should answer:

- is this still a basic small-prime residue-derived view
- does it preserve dependency on the center-analysis foundation
- does it keep custom tracked primes as a bounded inspection input rather than an unbounded analysis dimension
- does it avoid drifting into generic wheel-engine or sieve-layer design
- does it remain locally testable before any API work begins


