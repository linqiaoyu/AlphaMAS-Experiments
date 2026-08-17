# A1 Formal research freeze

`A1_NO_ONLINE_ADAPTATION` is permanently research-frozen after a correctness-
valid 78/78 Formal result. The frozen source is commit
`11ae1ce4a3bac6245dbc39c073bcfc2ac0bba16b` on
`ablation/a1-no-online-adaptation`; the configuration, preregistration, policy
identity, and fast identity are recorded in `a1_research_freeze.json`.

The official lineage remains `20260817T132343821395Z_11ae1ce4`. The clean
Recovery #2 boundary was mechanically recovered without replacing any completed
case, and the same lineage completed the remaining cases under `--resume`.

The final result is AAPL 26, AMZN 26, JPM 26, total 78, failures 0. A1 credits
are scored and archived without online parameter updates. Policy and fast
identities are unchanged from the initial state; optimiser steps and all
parameter/global/cross-symbol mutations are zero.

No A2, ARMA, or COMPARE run is part of this freeze. The final EC2 resource is
stopped after archive verification, with persistent EBS preserved and zero
running or pending AlphaMAS `g5.xlarge` instances. The final
archive inventory and document identities are recorded in `SHA256SUMS` and the
handoff commit.

**Verdict: PASS**
