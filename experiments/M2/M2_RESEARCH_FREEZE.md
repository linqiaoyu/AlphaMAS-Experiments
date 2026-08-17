# M2 Research Freeze

Freeze timestamp: `2026-08-17T12:07:04Z`.

**Full M2 official result is permanently frozen.**

The authoritative Formal source is
`6306ea4ea20cda501c6238db80c34d27bbc16bea`. The official Formal archive commit
is `63b2ed2d98d954b4eaa7815c08f1e9fdef8aa4e0`, and the official run is
`20260817T101217082243Z_6306ea4e` for `M2_agentic_rl_2024H1`.

The immutable result is AAPL 26/26, AMZN 26/26, JPM 26/26, total 78/78, with
zero decision failures and final validation `PASSED`. The archive inventory
identity is `a783f1a940ab69700bb5612642885ba040c94edfa13fb9d8ab2b448cdf87dd77`.
The final Post-run Audit identity is
`2806edebcc2103f4c8a5f2efe5b9f0c3b027eecc79fc888f380a354713e00691`.

## Frozen research identities

- M1 information bundle:
  `30596a54788101873f1c88bdf653df7f12ac3b4861a7058b6a36df0861274121`
- Semantic representation:
  `6e3b11863bc3ec214444326a269477e465101afb866f30e80698f37c7148d2fe`
- Global policy: C09, parameter
  `6baafc03b0b63512b3a66a1ae8f1ce1ce7e774395787626b49905e7b72cd1841`,
  model `56dc52128e1df9c9ddcf79fa6f7b293393bd61306ba4ef032f96cad6bf92126c`
- Online adaptation: O08, learning rate `1e-3`, two epochs per matured credit,
  AdamW, weight decay `1e-4`, gradient clip `0.5`, 165 per-symbol fast parameters
- Reward: `R3_HOLD_RELATIVE_DRAWDOWN_UTILITY`
- Method: `M2-PA-CTPPO-v2`
- Counterfactual tree contract: `M2_TRAIN_COUNTERFACTUAL_TREE-v2`

## Same-lineage closure

The preserved official history contains ten operational interruptions and ten
safe resumes across 11 attempts. Every accepted resume remained within Memory
lineage `20260816T150158003630Z_6306ea4e`, ending at Formal lineage
`20260817T101217082243Z_6306ea4e`. Torn states were restored only to proved exact
pre-case boundaries. Completed cases regenerated: 0. Completed cases replaced: 0.
There is no competing official trajectory.

Complete recoverable same-lineage DeepSeek usage is 2,345 requests, 24,961,617
input tokens, 3,127,030 output tokens, and CNY 24.08240596. This includes the
preserved two partial failed-attempt records; no missing usage is silently
estimated. Estimated Formal AWS use is 38,319 running seconds, 10.64416667
GPU-hours, and USD 13.59260083 at USD 1.277/hour. The canonical `g5.xlarge` is
stopped, with zero running or pending AlphaMAS `g5.xlarge` instances.

## Canonical A1/A2 definitions

The authoritative preregistration identity is
`e7e2cc8520f9033e57c442b04c882baffd7c51b497bbc9495b71098f64a83b0e`.
Observed M2 performance did not redefine either ablation.

`A1_NO_ONLINE_ADAPTATION` is Full M2 minus only delayed per-symbol online
fast-parameter updates. It starts from exact C09 and preserves the full M2
Actor/Critic, R3, Prompt prior, semantic representation, M1 information, Risk
Debate, Portfolio Manager, execution, and Formal protocol. Credits may be
recorded and scored for audit but cannot update parameters.

`A2_NO_GLOBAL_PRETRAINING` is Full M2 minus global C09 pretraining. It starts
from the exact frozen M2-11 initial-model parameter SHA
`60a0fec7b69ef2d0576a9c0894be09c377d573585db827c162279fb27483303e` and
retains O08 without retuning, semantic representation, R3, Prompt prior, online
chronology, Risk Debate, Portfolio Manager, execution, and Formal protocol.

The remote branches `baseline-m2`, `ablation/a1-no-online-adaptation`, and
`ablation/a2-no-global-pretraining` all point exactly to the frozen Formal source
SHA. A1 and A2 therefore begin with zero implementation delta. The legacy
`ablation/no-memory` and `ablation/reward-pnl-only` branches remain untouched.

Formal M2 must never be rerun because of performance. Performance must not be
used to change C09, O08, R3, representation, prompts, Agent graph, protocol,
checkpoint, hyperparameters, or the official result. Any exploratory redesign
must be a separate non-M2 experiment. Comparative interpretation remains
deferred to `COMPARE-01`.

## Locked route

1. `A1-01` — implement and pre-Formal freeze `A1_NO_ONLINE_ADAPTATION`
2. `A1-02` — Formal A1, Post-run Audit, and research freeze
3. `A2-01` — implement and pre-Formal freeze `A2_NO_GLOBAL_PRETRAINING`
4. `A2-02` — Formal A2, Post-run Audit, and research freeze
5. `ARMA-01` — frozen ARMA(1,1) benchmark
6. `COMPARE-01` — final controlled comparative analysis

M2 is closed. A1-01 has not started in M2-16.
