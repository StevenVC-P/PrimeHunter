# Missing Partner Analysis Review Guide

## Why This Tool Exists

This tool is the second PrimeHunter v1 tool and the first clearly derived tool built on top of the center-analysis foundation.

It exists to isolate and study cases where:

- one side of a center is prime
- the other side is composite
- the pair therefore fails to be a twin prime

This makes it a focused explanation tool for near-miss twin-prime cases.

## Canonical Scope

This tool currently covers:

- filtering canonical center-analysis records down to missing-partner cases
- summary counts for left-missing vs right-missing cases
- smallest disruptor frequency summaries across missing-partner failures
- local JSON result-envelope writing
- summary-only local runs for larger ranges

It does not yet cover:

- deeper factor pattern breakdowns
- residue-derived missing-partner views
- API access
- performance work beyond hard limits

## Package Layout

- `tool.py`
  Core filtering and summary-only range analysis.

- `statistics.py`
  Summary generation for filtered missing-partner records.

- `json_outputs.py`
  Canonical JSON envelope and local JSON writing.

## Dependency Rule

This tool depends on the center-analysis foundation.

That dependency is intentional.
This tool should remain derived from canonical center-analysis records rather than duplicating core classification logic.

## Entry Point

Human/dev runner:

- `scripts/tools/missing_partner_analysis_experiment.py`

Current command examples:

```powershell
python -m scripts.tools.missing_partner_analysis_experiment
python -m scripts.tools.missing_partner_analysis_experiment --start-n 1 --end-n 20
python -m scripts.tools.missing_partner_analysis_experiment --start-n 1 --end-n 1000000 --summary-only
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
- summary-only mode returns aggregate missing-partner data only

## Review Expectations For Agents

When reviewing or extending this tool, check:

- does it only return `left_only_prime` and `right_only_prime` cases in full-record mode
- does it remain derived from center-analysis records instead of reimplementing the foundation
- do summaries correctly count left-missing and right-missing cases
- do smallest-disruptor frequencies reflect the composite side only
- does JSON remain the canonical output
- do hard limits remain enforced

## Extension Rule

Any future extension should answer:

- is this still a derived missing-partner tool
- does it preserve dependency on the canonical center-analysis model
- does it avoid drifting into a second implementation of the center-analysis foundation
- does it remain locally testable before any API work begins


