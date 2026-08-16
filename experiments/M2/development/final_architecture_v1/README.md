# M2-14 Phase-A architecture and ablation archive

This archive was committed before any paid E2E_PILOT call or pilot-performance inspection. It binds the production M2 Trader architecture, the A1/A2 preregistration, and the one-shot E2E execution plan to the canonical machine-readable records in AlphaMAS source.

- Architecture: `M2-FINAL-ARCHITECTURE-v1`, identity `35c5a46616f654ce70b0badc01cd59fb0afd433dcdcd99e5e0b8f2419ec4d153`.
- Ablations: `M2-ABLATION-PREREGISTRATION-v1`, identity `e7e2cc8520f9033e57c442b04c882baffd7c51b497bbc9495b71098f64a83b0e`.
- Pilot population: exactly eight frozen `E2E_PILOT` cases at `2023-10-06`.
- Protected status: zero FINAL_HOLDOUT and Formal 2024H1 Agent executions; neither result population inspected.

The complete AlphaMAS records are `docs/m2/m2_final_architecture_freeze.json`, `docs/m2/m2_ablation_preregistration.json`, and `docs/m2/m2_e2e_pilot_execution_plan.json`. `phase_a_registry.json` contains the archive-side equivalent research binding. Its final source and Experiments commit fields are completed only by the immutable Git commit identities themselves and the Phase-A remote-verification record created at the commit barrier.
