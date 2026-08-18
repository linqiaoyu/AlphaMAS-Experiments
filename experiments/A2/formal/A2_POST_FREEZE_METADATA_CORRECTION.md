# A2 Post-Freeze Metadata Correction

This record documents one transparent metadata-only correction after the A2
research freeze.

## Correction

- Original freeze commit: `1609e606307db94f333fd81d83c839316066417c`
- Affected file: `A2_POST_RUN_AUDIT.json`
- Field: `population.decision_cache_cases`
- Original value: `0`
- Corrected value: `78`
- Classification: `AUDIT_METADATA_COUNTING_ERROR`
- Rerun performed: NO

## Mechanical counting method

The official archived runtime DecisionCache was traversed by its content-addressed
case directories. An entry was counted only when the repository `DecisionCache`
loader accepted it with required artifacts and usage, its `run_status.json` was
`success`, its `decision.json` status was `success`, and the embedded cache key
matched the directory key. Symbol and decision-session pairs were then checked for
uniqueness and reconciled to the complete Formal case artifacts.

## Evidence

- AAPL successful DecisionCache cases: 26
- AMZN successful DecisionCache cases: 26
- JPM successful DecisionCache cases: 26
- Total successful DecisionCache cases: 78
- Complete Formal case artifacts: 78
- Formal case-level source-audit files: 78
- Missing Formal cases: 0
- Duplicate Formal cases: 0
- Invalid Formal cases: 0
- DecisionCache entries failing completeness checks: 0
- DecisionCache symbol/date pairs absent from Formal cases: 0
- Formal symbol/date pairs absent from DecisionCache: 0
- Archive validator: PASS
- Official bundle inventory: 7,631/7,631 verified; mismatch 0
- Same-lineage committed cases regenerated: 0
- Same-lineage committed cases replaced: 0

The physical DecisionCache and complete Formal artifacts therefore establish that
the archived value `0` was an audit metadata counting error. It was not missing
runtime data, a missing cache, a corrupted Formal run, a source bug, or an
experiment correctness failure.

## Research invariance

- Official trajectory changed: NO
- Formal decision changed: NO
- Metric changed: NO
- Memory changed: NO
- RL state changed: NO
- Source changed: NO
- Archive official bundle changed: NO
- Rerun performed: NO

This correction changes audit metadata only. It does not alter the frozen A2
Formal trajectory, results, treatment, source, runtime state, or research
interpretation.
