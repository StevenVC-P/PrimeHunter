# Center Analysis Tool

## Purpose

This is the first canonical PrimeHunter v1 tool.

It analyzes twin-prime centers of the form `6n`, evaluates the left and right candidates, classifies each center, records smallest disruptors for composite sides, and writes structured local JSON results.

## Main Files

- `primehunter/tools/center_analysis/`
  Tool package.

- `center_analysis_experiment.py`
  Local runner for generating test output.

## Status

- built: yes
- tested: partial
- deployed: internal-only

## How To Run

Default run:

```powershell
python center_analysis_experiment.py
```

Run a smaller range:

```powershell
python center_analysis_experiment.py --start-n 1 --end-n 20
```

Run in summary-only mode:

```powershell
python center_analysis_experiment.py --start-n 1 --end-n 1000000 --summary-only
```

Write to a custom path:

```powershell
python center_analysis_experiment.py --start-n 1 --end-n 50 --output outputs/center_analysis/sample.json
```

## Output

Default output files:

- full-record mode: `outputs/center_analysis/twin_center_analysis.json`
- summary-only mode: `outputs/center_analysis/twin_center_analysis_summary.json`

The tool writes structured JSON only.
Text printed to the terminal is summary-only.

When `--summary-only` is used, the JSON output still contains the normal envelope and summary block, but `records` is written as an empty list.

The output now also includes metadata describing:

- generation time
- mode
- record limit
- summary limit
- requested range

## Current Limits

- local/internal use only
- no API surface yet
- wheel is fixed to `6`
- analysis is currently range-based by `n`
- no residue or sieve-derived views included yet
- full-record mode hard limit: `100000` centers
- summary-only mode hard limit: `1000000` centers
- CLI integers must be plain digits, not comma-formatted values

## Current Success Condition

This tool is considered successful at the current stage when it:

- runs locally
- writes valid structured JSON
- follows the canonical center record shape
- correctly computes classifications and smallest disruptors
