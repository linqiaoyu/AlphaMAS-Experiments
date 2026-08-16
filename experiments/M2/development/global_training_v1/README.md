# M2-11 TRAIN-only global PA-CTPPO-v2 training

Status: complete and correctness-valid. The preregistration commit preceded all
real TRAIN optimisation.

This plan binds the exact frozen `M2-PA-CTPPO-v2` method, the canonical v2
counterfactual tree, seed 20260816, one canonical initial checkpoint, three
learning rates, and checkpoints at outer iterations 25, 50, and 100. Exactly
nine candidates will be generated. All three canonical LR lineages must finish
before three audit-only deterministic replays begin.

The only optimisation population is the 8,744 reachable TRAIN tree nodes and
their 26,232 raw local R3 action credits. Full-tree exact action expectation is
mandatory. There is no Validation optimisation or candidate comparison, no
Final Holdout/E2E Pilot/Formal access, no action sampling, no minibatching, no
Bellman bootstrap, no gamma, no GAE, and no reward or advantage transformation.

## Frozen execution bindings

- Starting source: `e37456f871b461ed913a13501805f99750e41b0b`
- Starting experiments: `1569c97d3285b5f5e22c21fb1e97c00b1ed015c8`
- Trainer: `178746e23ff8cf0195529fc92adf5f7b533d24d3`
- Initial model parameter SHA: `60a0fec7b69ef2d0576a9c0894be09c377d573585db827c162279fb27483303e`
- Tree: `ff5e1bf21ef90b9eeec96d257c59e83656957f32ec4d2f94396a0a5d4bf1db13`
- Representation: `6e3b11863bc3ec214444326a269477e465101afb866f30e80698f37c7148d2fe`
- Reward: `R3_HOLD_RELATIVE_DRAWDOWN_UTILITY`

The existing London `g5.xlarge` and encrypted persistent EBS workspace will be
reused. A conservative one-hour estimate for canonical training plus one hour
for replay is USD 2.574 including a small storage/transfer allowance, below the
M2-11 USD 5 ceiling. The existing 90-minute auto-stop remains enabled; canonical
and replay execution are split into separate bounded sessions if necessary.

Candidate selection is not performed here. The frozen Validation selection rule
remains dormant and selection is deferred to M2-12.

## Completion

All three canonical LR lineages and all three audit-only replay lineages completed
100 outer iterations with four frozen-old-policy epochs per iteration. The audit
covered 300 canonical and 300 replay outer iterations. All nine replay checkpoint
parameter SHAs match their canonical counterparts exactly; stale-policy,
within-block-refresh, NaN, Inf, occupancy, and parameter-count violations are zero.
The maximum weighted counterfactual-advantage residual is
`1.734723475976807e-17`.

The archive contains exactly C01–C09. No candidate has been ranked, preferred,
recommended, discarded, or selected. Validation performance, Final Holdout,
E2E Pilot performance, and Formal 2024 results were not accessed. Replay
checkpoints are audit-only and not selection-eligible.
