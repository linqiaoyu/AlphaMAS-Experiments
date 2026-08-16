# M2-13 TRAIN-only online adaptation

This archive freezes the preregistered M2-13 delayed per-symbol online
adaptation study. Phase A contains only this README and the machine-readable
plan. No complete O01–O09 TRAIN candidate performance had been inspected when
Phase A was committed.

The official Phase-B run consumed only the frozen TRAIN counterfactual tree and
byte-identical C09 checkpoint. Historical M2-12 VALIDATION result files remain
sealed and unchanged. Candidate-specific TRAIN-adapted states are audit
endpoints only and are not future model checkpoints.

The first complete correctness-valid run selected O08 (online LR `1e-3`, two
epochs) through the preregistered Prompt-override-rate tie-break after all nine
candidates tied on the primary and worst-symbol metrics. The one `AUDIT_ONLY`
replay reproduced every action, score, chronology record, and the selection.
