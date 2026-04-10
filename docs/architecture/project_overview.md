# Primehunter Project Overview

## What This Project Is

Primehunter is a small research-style Python project for exploring how primes can be generated or rediscovered using Euclid-style constructions.

The core idea is:

- start from a small seed set of known primes
- form products from those known primes
- examine `product + 1`
- see whether that step reveals new primes directly or through factorization

This project is not trying to replace standard prime-generation algorithms. Instead, it is meant to explore patterns in prime discovery, especially questions like:

- how far can we get starting from only `2`?
- what changes when repeated prime factors are allowed?
- what changes when composite results are factored instead of discarded?
- which primes are missed under weaker rules?

## What The Project Already Contains

The project currently has two main parts:

1. Reference prime-list generation
2. Euclid-style experiment scripts

### 1. Reference prime-list generation

The project includes a simple script for generating a master list of known primes in a range.

Current script:

- [primes.py](d:\Primehunter\primes.py)

Current output:

- [primes_master_10000.txt](d:\Primehunter\primes_master_10000.txt)

Right now, `primes.py` writes the master list of primes below `10,000`. This gives the project a baseline reference list that experiments can compare against.

### 2. Euclid-style experiment scripts

The repo now contains multiple experiment scripts so different rule sets can be tested independently.

Current experiment scripts:

- [euclid_experiment.py](d:\Primehunter\euclid_experiment.py)
- [euclid_square_free_experiment.py](d:\Primehunter\euclid_square_free_experiment.py)
- [euclid_square_free_no_factor_experiment.py](d:\Primehunter\euclid_square_free_no_factor_experiment.py)
- [reciprocal_cycle_experiment.py](d:\Primehunter\reciprocal_cycle_experiment.py)
- [run_experiment.py](d:\Primehunter\run_experiment.py)
- [compare_modes.py](d:\Primehunter\compare_modes.py)

These scripts all start from the seed `[2]` and currently test discoveries below `1000`, but they differ in how strict the construction rules are.

## Reciprocal Cycle Experiment

Script:

- [reciprocal_cycle_experiment.py](d:\Primehunter\reciprocal_cycle_experiment.py)

Shared helper module:

- [reciprocal_cycle_utils.py](d:\Primehunter\reciprocal_cycle_utils.py)

This experiment studies reciprocal cycle behavior for each prime `p > 3` in user-selected bases.

Default bases:

- `6`
- `12`

For each prime in range, it currently computes:

- `ord_p(6)`
- `ord_p(12)`
- `ord_p(6) / (p - 1)`
- `ord_p(12) / (p - 1)`
- whether `p - 2` is prime
- whether `p + 2` is prime
- whether the prime belongs to a twin-prime pair

Primes that are not coprime to a requested base are skipped automatically for that run.

Optional mode:

- generate the repeating expansion of `1/p` in each requested base

Outputs:

- JSON export
- CSV export
- optional text report

Terminal summary includes:

- how many primes were analyzed
- how many twin primes were present in range
- maximal-order counts for each requested base
- maximal-order counts restricted to twin primes

## Current Experiment Modes

### Full Euclid-style exploration

Script:

- [euclid_experiment.py](d:\Primehunter\euclid_experiment.py)

Rules:

- repeated prime factors are allowed
- composite `product + 1` values are factored

Example:

- `2^6 + 1 = 65 = 5 * 13`

This mode can discover new primes even when `product + 1` is not itself prime.

Current result below `1000`:

- finds all `168` primes below `1000`
- misses `0`

Output file:

- [primes_output.txt](d:\Primehunter\primes_output.txt)

### Square-free with factorization

Script:

- [euclid_square_free_experiment.py](d:\Primehunter\euclid_square_free_experiment.py)

Rules:

- each prime can appear at most once in a product
- composite `product + 1` values are factored

This keeps the subgroup products square-free while still using factorization to reveal hidden primes.

Current result below `1000`:

- finds `114` of `168` primes
- misses `54`

Output file:

- [primes_square_free_output.txt](d:\Primehunter\primes_square_free_output.txt)

### Square-free without factorization

Script:

- [euclid_square_free_no_factor_experiment.py](d:\Primehunter\euclid_square_free_no_factor_experiment.py)

Rules:

- each prime can appear at most once in a product
- composite `product + 1` values are discarded

This is the strictest and weakest version.

Current result below `1000`:

- finds `4` of `168` primes
- misses `164`

Output file:

- [primes_square_free_no_factor_output.txt](d:\Primehunter\primes_square_free_no_factor_output.txt)

## Shared Helper Modules

The project already has shared helper files so logic is not duplicated between scripts.

### Prime helpers

- [prime_utils.py](d:\Primehunter\prime_utils.py)

This file contains reusable low-level prime utilities:

- primality checking
- generating all primes below a limit
- prime factorization

### Reciprocal cycle helpers

- [reciprocal_cycle_utils.py](d:\Primehunter\reciprocal_cycle_utils.py)

This file contains reusable reciprocal-cycle utilities:

- multiplicative order modulo prime
- repeating expansion generation in user-selected bases
- twin-prime classification
- experiment summaries
- JSON, CSV, and text export helpers

### Euclid experiment helpers

- [euclid_utils.py](d:\Primehunter\euclid_utils.py)

This file contains the shared Euclid-style experiment engine:

- candidate generation
- repeated-factor vs. square-free toggles
- factorization toggle
- discovery tracking
- report writing

This means new experiments can be added with small wrapper scripts instead of rewriting the algorithm each time.

## New CLI Workflow

The project now includes a unified command-line runner:

- [run_experiment.py](d:\Primehunter\run_experiment.py)

This runner supports:

- `--mode`
- `--seed`
- `--limit`
- `--format`
- `--output`

It can write:

- text reports
- JSON exports
- CSV discovery logs

The project also now includes a side-by-side mode comparison tool:

- [compare_modes.py](d:\Primehunter\compare_modes.py)

That script can run multiple experiment modes with the same seed and limit and generate a comparison summary in text or JSON form.

It can also now generate both formats at once, so one command can produce:

- a human-readable text summary
- a machine-readable JSON comparison bundle

## Comparison Document

The project already contains a comparison write-up for the three current experiment modes:

- [euclid_experiment_comparison.md](d:\Primehunter\euclid_experiment_comparison.md)

That document summarizes:

- the rules of each experiment
- how many primes each mode finds below `1000`
- how many each mode misses
- the main takeaway about repeated factors and factorization

## What The Project Is Good For Right Now

At its current stage, the project is useful for:

- generating a reference list of primes up to a chosen limit
- testing Euclid-style prime discovery rules
- comparing stricter vs. looser construction rules
- seeing which primes are found directly and which are revealed through factorization
- studying how repeated prime factors affect coverage

## Current Limitations

The project is still exploratory, so it also has some current limitations:

- limits are currently hard-coded in the scripts
- starting seeds are currently fixed in the runner scripts
- outputs are written as plain text reports rather than structured data
- there is not yet a single command-line interface for choosing mode, seed, or limit
- there is not yet a larger-scale study beyond the current `1000` and `10,000` checkpoints

## Possible Next Steps

Natural next improvements for this repo would be:

- make the seed list configurable from the command line
- make the search limit configurable from the command line
- add experiments for larger ranges such as `5000`, `10000`, or higher
- add a side-by-side summary report across all modes automatically
- separate direct-prime discoveries from factorization-based discoveries in the reports
- export results as CSV or JSON for further analysis

## Quick Run Commands

Current commands:

- `python primes.py`
- `python euclid_experiment.py`
- `python euclid_square_free_experiment.py`
- `python euclid_square_free_no_factor_experiment.py`
- `python reciprocal_cycle_experiment.py --bases 6,12 --limit 1000 --format json`
- `python reciprocal_cycle_experiment.py --bases 10 --limit 1000 --format csv`
- `python reciprocal_cycle_experiment.py --limit 1000 --format all --output reciprocal_cycles`
- `python reciprocal_cycle_experiment.py --bases 6,12,18 --limit 200 --include-expansions --format json`
- `python run_experiment.py --mode full --seed 2 --limit 1000`
- `python run_experiment.py --mode square_free_factor --seed 2,3 --limit 5000 --format json`
- `python compare_modes.py --seed 2 --limit 1000`
- `python compare_modes.py --seed 2 --limit 1000 --format all --output comparison_bundle`

These generate the current reference file and experiment reports in the project root.
