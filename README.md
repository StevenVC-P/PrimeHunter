# PrimeHunter

PrimeHunter is a Python backend engine for prime and twin-prime structural analysis. It is designed as a computation layer for mathematical experiments, modular pattern analysis, and structured data exports that can later support external tools such as visual explorers or APIs.

The project is guided by [PRIMEHUNTER_SPEC.md](PRIMEHUNTER_SPEC.md), which defines the long-term direction: pure math helpers, higher-level structural analysis, and data-oriented outputs.

## Current Focus

PrimeHunter currently supports two main research directions:

- Euclid-style prime discovery experiments
- Reciprocal-cycle analysis across primes and bases

These tools are meant for exploration and structural investigation rather than replacing optimized production prime-generation algorithms.

## Project Layout

### Core package

- `primehunter/math_core/`
  Pure deterministic math helpers such as primality testing and factorization.

- `primehunter/analysis/`
  Experiment logic and higher-level structural analysis.

- `primehunter/data/`
  Exporters and report writers for text, JSON, and CSV outputs.

### Supporting folders

- `docs/`
  Architecture notes and research write-ups.

- `outputs/`
  Generated experiment artifacts.

- `tests/`
  Reserved for automated coverage as the math tools stabilize.

- `scripts/`
  Reserved for helper tooling and developer automation.

## Available Entry Points

- `primes.py`
  Writes a canonical reference list of primes below a chosen limit.

- `run_experiment.py`
  Unified CLI for Euclid-style experiment modes.

- `compare_modes.py`
  Compares Euclid-style modes side by side.

- `reciprocal_cycle_experiment.py`
  Studies multiplicative order and reciprocal-cycle structure across primes.

- `euclid_experiment.py`
- `euclid_square_free_experiment.py`
- `euclid_square_free_no_factor_experiment.py`
  Thin mode-specific wrappers retained for convenience.

## Quick Start

Create or activate a virtual environment, then run any of the project entry points with Python.

Example commands:

```powershell
python primes.py
python run_experiment.py --mode full --seed 2 --limit 1000 --format json
python compare_modes.py --seed 2 --limit 1000 --format all
python reciprocal_cycle_experiment.py --bases 6,12 --limit 1000 --format json
```

Generated outputs are written under `outputs/` by default:

- `outputs/reference/`
- `outputs/euclid/`
- `outputs/reciprocal_cycles/`
- `outputs/comparisons/`

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
