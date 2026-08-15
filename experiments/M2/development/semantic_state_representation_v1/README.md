# M2-09 semantic state representation

This pre-Formal development archive freezes `M2-SEMANTIC-STATE-v1` from the immutable
56 TRAIN and 16 VALIDATION states in `M2-SEMANTIC-HANDOFF-v1`. Representation selection is
outcome-independent: only TRAIN embedding geometry may select the dimension. Rewards,
trading outcomes, validation performance, FINAL_HOLDOUT and E2E_PILOT are excluded.

The preregistered plan is committed before canonical inference. Encoder outputs and final
manifests are added only after the AWS double-run audit passes.

## Frozen result

- Encoder: `Qwen/Qwen3-Embedding-0.6B` at revision
  `97b0c614be4d77ee51c0cef4e5f07c00f9eb65b3`, permanently frozen.
- Canonical population: 56 TRAIN then 16 VALIDATION rows in the M2-08 manifest order.
- Dimension selector: TRAIN-only geometry over manager, trader and joint views.
- Selected dimension: 1024; 256 and 512 failed preregistered fidelity thresholds.
- Semantic base: `concat(z_RM, z_PT, z_PT-z_RM, dot(z_RM,z_PT), action_onehot)`,
  dimension 3076.
- Runtime portfolio state: `[is_cash, is_long, entry_log_return, current_drawdown]`,
  dimension 4.
- Future Actor observation: dimension 3080.
- Canonical inference audit: two byte-identical float32 runs; no truncation.
- Representation identity:
  `6e3b11863bc3ec214444326a269477e465101afb866f30e80698f37c7148d2fe`.

No reward, financial outcome, validation performance, FINAL_HOLDOUT state, or E2E_PILOT
state was read or used. Model weights remain outside Git in the persistent Hugging Face cache.
