# Formal M1 launch policy

> **One intended Formal M1 run. Its first complete correctness-valid 78-case trajectory is the sole official M1 result.**

- Performance-based rerun: **FORBIDDEN**.
- Same-lineage safe resume after a genuine infrastructure interruption: **ALLOWED**.
- Correctness failure: preserve the invalid/failed trajectory and stop for explicit review.
- Official `--force`: **FORBIDDEN**.
- Execution: one runner, one experiment lifecycle, one Memory lineage, one DecisionCache namespace, one artifact lifecycle.
- Symbol order: `AAPL → AMZN → JPM`; no parallel symbol writers.
- Launch is outside this task. No Formal M1 request was made during freeze.

