# PrimeHunter

PrimeHunter is a Python backend engine for prime and twin-prime structural analysis. It is designed as a computation layer for mathematical experiments, modular pattern analysis, and structured data exports that can later support external tools such as visual explorers or APIs.

The project is guided by [PRIMEHUNTER_SPEC.md](PRIMEHUNTER_SPEC.md), which defines the long-term direction: pure math helpers, higher-level structural analysis, and data-oriented outputs.

## Current Focus

PrimeHunter currently supports two main research directions:

- Euclid-style prime discovery experiments
- Reciprocal-cycle analysis across primes and bases

PrimeHunter also now includes the first v1 tool-family runners for:

- twin center analysis
- missing partner analysis
- residue-view analysis

These tools are meant for exploration and structural investigation rather than replacing optimized production prime-generation algorithms.

## Project Layout

### Core package

- `primehunter/math_core/`
  Pure deterministic math helpers such as primality testing and factorization.

- `primehunter/analysis/`
  Experiment logic and higher-level structural analysis.

- `primehunter/data/`
  Exporters and report writers for text, JSON, and CSV outputs.

- `primehunter/tools/`
  Canonical v1 tool packages.

- `primehunter/compat/`
  Compatibility wrappers retained for older import paths.

### Supporting folders

- `docs/`
  Architecture notes and research write-ups.

- `outputs/`
  Generated experiment artifacts.

- `tests/`
  Automated coverage for current tools and analysis helpers.

- `scripts/`
  Runnable entry points grouped by purpose.

## Script Layout

- `scripts/tools/`
  Local runners for the current PrimeHunter v1 tools.

- `scripts/research/`
  Older Euclid and reciprocal-cycle experiment runners.

- `scripts/reference/`
  Reference-data generators such as the master prime list writer.

## Available Entry Points

- `scripts/reference/primes.py`
  Writes a canonical reference list of primes below a chosen limit.

- `scripts/tools/center_analysis_experiment.py`
  Runs canonical twin-center analysis.

- `scripts/tools/missing_partner_analysis_experiment.py`
  Runs missing-partner analysis.

- `scripts/tools/residue_view_experiment.py`
  Runs the residue-view analysis tool.

- `scripts/research/run_experiment.py`
  Unified CLI for Euclid-style experiment modes.

- `scripts/research/compare_modes.py`
  Compares Euclid-style modes side by side.

- `scripts/research/reciprocal_cycle_experiment.py`
  Studies multiplicative order and reciprocal-cycle structure across primes.

- `scripts/research/euclid_experiment.py`
- `scripts/research/euclid_square_free_experiment.py`
- `scripts/research/euclid_square_free_no_factor_experiment.py`
  Thin mode-specific wrappers retained for convenience.

## Quick Start

Create or activate a virtual environment, then run any of the project entry points with Python.

Example commands:

```powershell
python -m scripts.reference.primes
python -m scripts.tools.center_analysis_experiment --start-n 1 --end-n 100
python -m scripts.tools.missing_partner_analysis_experiment --start-n 1 --end-n 100
python -m scripts.tools.residue_view_experiment --start-n 1 --end-n 100 --primes 5,7,11
python -m scripts.research.run_experiment --mode full --seed 2 --limit 1000 --format json
python -m scripts.research.compare_modes --seed 2 --limit 1000 --format all
python -m scripts.research.reciprocal_cycle_experiment --bases 6,12 --limit 1000 --format json
```

Generated outputs are written under `outputs/` by default:

- `outputs/reference/`
- `outputs/euclid/`
- `outputs/reciprocal_cycles/`
- `outputs/comparisons/`
- `outputs/center_analysis/`
- `outputs/missing_partner_analysis/`
- `outputs/residue_view/`

## Example Research Questions

- How much prime coverage do Euclid-style constructions achieve under different rules?
- Which primes are missed when repeated factors are disallowed?
- How often do twin primes show maximal multiplicative order in selected bases?
- What modular patterns appear when primes are viewed as survivors of layered constraints?

## Documentation

- [PRIMEHUNTER_SPEC.md](PRIMEHUNTER_SPEC.md)
- [Project Overview](docs/architecture/project_overview.md)
- [Project Structure](docs/architecture/PROJECT_STRUCTURE.md)
- [Euclid Experiment Comparison](docs/research/euclid_experiment_comparison.md)

## Status

PrimeHunter is still in an exploratory stage. The current codebase is organized for growth, and the next steps are expected to add more math tools, more experiments, and stronger automated tests.

