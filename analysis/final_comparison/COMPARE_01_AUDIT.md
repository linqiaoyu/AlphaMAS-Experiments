# COMPARE-01 Audit

**Verdict: PASS**

- Six official systems resolved; freeze/validation status: PASS for M0, M1, M2, A1, A2 and ARMA.
- Anchor values: all exact matches within 1e-15.
- Decision populations: 78 each (26 per AAPL/AMZN/JPM); failures: 0.
- Comparability contract: PASS; market snapshot identities exact.
- Terminal return recalculation: PASS for all systems, Equal-weight B&H and SPY; official metrics remain authoritative.
- Controlled return-delta anchors: exact; absolute differences from accepted COMPARE-01 are 0.
- Tables and figures derive only from frozen repository artifacts.
- Presentation-unit audit: percentage levels `%` PASS; percentage-level differences `pp` PASS; ratios unitless PASS.
- Official metric values changed: NO; controlled-delta values changed: NO; scientific conclusions changed: NO.
- Source experiment modifications: 0; new experimental decisions/model fits: 0.
- DeepSeek calls: 0; Qwen calls: 0; AWS starts: 0; GPU-hours: 0; paid cost: $0.
- Statistical tests/p-values: 0; no significance claim; no formal interaction claim.
- M3 introduced: NO.
- AlphaMAS: `compare-with-adft` at `d6c2b11cc4646dc06c435fe10a027d8f867e2791`, clean.
- Experiments branch: `analysis/final-comparison`; branch base/main/origin-main: `ccd5cf5c4e4d244af252d58b94531348ca710678`.

Machine-readable detail is in `COMPARE_01_AUDIT.json` and `comparability_audit.json`.
