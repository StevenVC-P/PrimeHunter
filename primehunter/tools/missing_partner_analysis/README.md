# Missing Partner Analysis Tool

## Purpose

This tool is a derived PrimeHunter v1 tool built on canonical center-analysis records.

It focuses only on centers where exactly one side is prime and the other side is composite. These are the cases where a twin-prime pair almost forms but fails because one partner is missing.

## Main Files

- `primehunter/tools/missing_partner_analysis/`
  Tool package.

- `scripts/tools/missing_partner_analysis_experiment.py`
  Local runner for generating test output.

## Status

- built: yes
- tested: partial
- deployed: internal-only

## How To Run

Default run:

```powershell
python -m scripts.tools.missing_partner_analysis_experiment
```

Run a smaller range:

```powershell
python -m scripts.tools.missing_partner_analysis_experiment --start-n 1 --end-n 20
```

Run in summary-only mode:

```powershell
python -m scripts.tools.missing_partner_analysis_experiment --start-n 1 --end-n 1000000 --summary-only
```

Write to a custom path:

```powershell
python -m scripts.tools.missing_partner_analysis_experiment --start-n 1 --end-n 50 --output outputs/missing_partner_analysis/sample.json
```

## Output

Default output files:

- full-record mode: `outputs/missing_partner_analysis/missing_partner_analysis.json`
- summary-only mode: `outputs/missing_partner_analysis/missing_partner_analysis_summary.json`

The tool writes structured JSON only.
Text printed to the terminal is summary-only.

When `--summary-only` is used, the JSON output still contains the normal envelope and summary block, but `records` is written as an empty list.

## Current Limits

- local/internal use only
- no API surface yet
- wheel is fixed to `6`
- analysis is currently range-based by `n`
- full-record mode hard limit: `100000` centers
- summary-only mode hard limit: `1000000` centers
- CLI integers must be plain digits, not comma-formatted values
- this tool is derived from center-analysis records and does not replace the center-analysis foundation

## Current Success Condition

This tool is considered successful at the current stage when it:

- runs locally
- writes valid structured JSON
- returns only one-prime/one-composite center cases in full-record mode
- correctly summarizes missing-partner counts and disruptor frequencies


