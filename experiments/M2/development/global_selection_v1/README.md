# M2-12 Global Checkpoint Selection

STATUS: FROZEN — OFFICIAL M2-12 SELECTION COMPLETE

This directory preregisters the first and only VALIDATION selection among the
nine frozen M2-11 global PA-CTPPO-v2 candidates. The selection is static-policy,
sequential within symbol, and mechanical. No candidate may be trained, adapted,
replaced, or selected using Holdout, E2E, Formal, live-data, or historical
performance information.

The official first correctness-valid atomic run selected C09 mechanically on the
primary metric. No tie-break was invoked and `HUMAN_OVERRIDE = false`. The
`selection_audit.json` replay is audit-only and reproduced all 144 actions, all
selected-action R3 values, every primary score, the tie-break path, and C09.

M2-12 used VALIDATION only for the preregistered global checkpoint selection. No
candidate parameters were updated using VALIDATION.
