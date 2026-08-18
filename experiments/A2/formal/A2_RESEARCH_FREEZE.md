# A2 Research Freeze

Full A2 official result is permanently frozen.

This freeze binds the first complete correctness-valid A2 trajectory, completed at 78/78 with zero failures. It may not be rerun because of performance.

## Frozen bindings

- Source: `ae0f36b16a17a1321c17c630fb6a52e10dd23fcd`
- Formal config: `d8982296be9d632be996d23836cfebb7fb2fb363b6fd496590056025251a07da`
- Preregistration: `e7e2cc8520f9033e57c442b04c882baffd7c51b497bbc9495b71098f64a83b0e`
- Experiment: `A2_no_global_pretraining_2024H1`
- Official run: `20260818T204749061036Z_ae0f36b1`
- Memory lineage: `20260818T130800804933Z_ae0f36b1`
- Initial checkpoint file: `4d65dd2c1563b144aee8e79878171feb1ecd990a8bd8e2c584547eaa3a546c9f`
- Initial checkpoint parameters: `60a0fec7b69ef2d0576a9c0894be09c377d573585db827c162279fb27483303e`
- Representation: `6e3b11863bc3ec214444326a269477e465101afb866f30e80698f37c7148d2fe`
- Reward: `R3_HOLD_RELATIVE_DRAWDOWN_UTILITY`
- Online adaptation: frozen O08
- M1 Formal bundle: `30596a54788101873f1c88bdf653df7f12ac3b4861a7058b6a36df0861274121`
- Post-run Audit: `A2_POST_RUN_AUDIT.md` and machine-readable companion
- Artifact inventory: `A2_SHA256SUMS`, SHA `0106e17ddba6bde6687ee0ea5cd5f3ac06210f466c028b40033bac78615adcc3`

## Acceptance

AAPL 26/26, AMZN 26/26, JPM 26/26; total 78/78; failures 0. PIT, evidence, snapshot-only execution, accounting, global immutability, fast-only adaptation, exactly-once updates, per-symbol isolation, cache isolation, and Memory lineage validation passed. C09 was not loaded. The global/non-fast SHA remained `9b83aa1382d6b41c55981f2475eb0e236248affc5b5004a151a4b01651fa646e`; only the authorised 165 fast values evolved.

## Recovery and resources

Five operational EC2 auto-stop interruptions were resumed safely in the same lineage. Committed cases regenerated: 0. Committed cases replaced: 0. Competing trajectories: 0.

Complete same-lineage DeepSeek usage is 2,298 request records, 24,501,677 input tokens, 3,053,112 output tokens, 27,554,789 total tokens, and CNY 22.87189076. AWS accounting is six successful starts, 30,724 running seconds, 8.53444444 GPU-hours, and estimated USD 10.89848556. The canonical instance is stopped; running and pending AlphaMAS g5.xlarge counts are both zero.

ARMA-01 and COMPARE-01 were not started.

