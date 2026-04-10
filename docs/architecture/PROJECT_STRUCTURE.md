# PrimeHunter Project Structure

PrimeHunter now uses a project layout that separates code, documentation, generated artifacts, and future test coverage.

## Root Layout

- `PRIMEHUNTER_SPEC.md`
  - Primary project direction document kept at the repo root.

- `primehunter/`
  - Main Python package.

- `docs/`
  - Human-facing documentation and research notes.

- `outputs/`
  - Generated experiment artifacts and export files.

- `scripts/`
  - Reserved for future helper scripts, automation, or developer tooling.

- `tests/`
  - Reserved for automated test coverage.

## Package Layout

- `primehunter/math_core/`
  - Pure deterministic math helpers.

- `primehunter/analysis/`
  - Higher-level structural and experiment logic.

- `primehunter/data/`
  - Export, reporting, and structured output helpers.

## Docs Layout

- `docs/architecture/`
  - Project overview and organization docs.

- `docs/research/`
  - Research notes, comparisons, and experiment write-ups.

## Output Layout

- `outputs/reference/`
  - Canonical reference datasets such as prime lists.

- `outputs/euclid/`
  - Euclid-style experiment outputs.

- `outputs/reciprocal_cycles/`
  - Reciprocal-cycle analysis exports.

- `outputs/comparisons/`
  - Cross-mode and comparison outputs.

## Entry Points

The current root-level Python files remain as simple CLI entry points so the existing workflow stays easy:

- `primes.py`
- `run_experiment.py`
- `compare_modes.py`
- `euclid_experiment.py`
- `euclid_square_free_experiment.py`
- `euclid_square_free_no_factor_experiment.py`
- `reciprocal_cycle_experiment.py`

## Rule For New Work

1. Put pure math utilities in `primehunter/math_core/`.
2. Put modeling and experiment logic in `primehunter/analysis/`.
3. Put exporters and report writers in `primehunter/data/`.
4. Put narrative docs in `docs/`.
5. Put generated data in `outputs/`.
6. Add tests in `tests/` as new tools stabilize.
