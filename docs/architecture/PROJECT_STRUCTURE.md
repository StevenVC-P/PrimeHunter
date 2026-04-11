# PrimeHunter Project Structure

PrimeHunter uses a project layout that separates code, runnable scripts, documentation, generated artifacts, and tests.

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
  - Runnable entry points grouped by purpose.

- `tests/`
  - Automated test coverage.

## Package Layout

- `primehunter/math_core/`
  - Pure deterministic math helpers.

- `primehunter/analysis/`
  - Higher-level structural and experiment logic.

- `primehunter/data/`
  - Export, reporting, and structured output helpers.

- `primehunter/tools/`
  - Canonical v1 tool packages.

- `primehunter/compat/`
  - Compatibility wrappers for older imports.

## Scripts Layout

- `scripts/tools/`
  - Local runners for the current PrimeHunter v1 tools.

- `scripts/research/`
  - Euclid and reciprocal-cycle experiment entry points.

- `scripts/reference/`
  - Reference-data generators.

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

- `outputs/center_analysis/`
  - Center-analysis tool outputs.

- `outputs/missing_partner_analysis/`
  - Missing-partner tool outputs.

- `outputs/residue_view/`
  - Residue-view tool outputs.

## Entry Points

Runnable scripts now live under `scripts/` instead of the repository root:

- `scripts/reference/primes.py`
- `scripts/tools/center_analysis_experiment.py`
- `scripts/tools/missing_partner_analysis_experiment.py`
- `scripts/tools/residue_view_experiment.py`
- `scripts/research/run_experiment.py`
- `scripts/research/compare_modes.py`
- `scripts/research/euclid_experiment.py`
- `scripts/research/euclid_square_free_experiment.py`
- `scripts/research/euclid_square_free_no_factor_experiment.py`
- `scripts/research/reciprocal_cycle_experiment.py`

## Rule For New Work

1. Put pure math utilities in `primehunter/math_core/`.
2. Put modeling and experiment logic in `primehunter/analysis/`.
3. Put exporters and report writers in `primehunter/data/`.
4. Put canonical v1 tools in `primehunter/tools/`.
5. Put compatibility wrappers in `primehunter/compat/`.
6. Put runnable entry points in `scripts/`, not the repo root.
7. Put narrative docs in `docs/`.
8. Put generated data in `outputs/`.
9. Add tests in `tests/` as new tools stabilize.

