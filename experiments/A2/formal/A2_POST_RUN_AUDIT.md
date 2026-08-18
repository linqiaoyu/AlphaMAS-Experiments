# A2 Post-run Audit

Generated from the remotely verified official A2 bundle.

## Verdict

PASS. The first complete correctness-valid A2 trajectory completed at 78/78 with zero failures. Performance was not used for selection, rerun, or tuning.

## Identity

- Branch/source: `ablation/a2-no-global-pretraining` / `ae0f36b16a17a1321c17c630fb6a52e10dd23fcd`
- Config SHA: `d8982296be9d632be996d23836cfebb7fb2fb363b6fd496590056025251a07da`
- Preregistration: `e7e2cc8520f9033e57c442b04c882baffd7c51b497bbc9495b71098f64a83b0e`
- Experiment: `A2_no_global_pretraining_2024H1`
- Official completed run: `20260818T204749061036Z_ae0f36b1`
- First run: `20260818T130800804933Z_ae0f36b1`
- Memory lineage: `20260818T130800804933Z_ae0f36b1`
- Resolved config SHA: `ed9e25555e2d41c116785eaa89fd580ec41d12d1dcfee6e8f9f15be9e4f99e3e`
- Graph config SHA: `22d339e831a055b914932618de279fb72da9327b9bb875fecc86a02c20f0b0a8`

## Population and correctness

AAPL 26/26, AMZN 26/26, JPM 26/26; total 78/78; failures 0. The validation report is `passed`. It confirms the frozen schedule, Good Friday handling, next-valid-session open execution, final valuation 2024-07-05, no future market data, no same-bar execution, no negative cash, no shorting, no duplicate fills, complete daily equity, aligned benchmarks, dividend accounting, P&L identity, and finite metrics.

The four frozen market snapshot identities are preserved. The final archive contains 78 complete DecisionCache cases and 78 source-audit files.

## Initial checkpoint and A2 treatment

- Initial checkpoint file SHA: `4d65dd2c1563b144aee8e79878171feb1ecd990a8bd8e2c584547eaa3a546c9f`
- Initial checkpoint parameter SHA: `60a0fec7b69ef2d0576a9c0894be09c377d573585db827c162279fb27483303e`
- Initial runtime fast SHA: `49380bb69ea6fb7682fe97a3ef5e1ccf2b2429b749d6f9f9971e40725271fcf9`
- Initial canonical fast SHA: `859d91374903768e82c8d3621ca18ea6e8ba3b0002e9e915a579df13664e27d2`
- Initial optimiser identity: `087df628de120d7e2271432fe99d2888097983c25a3cfc880ec60a51d3b4d623`
- Initial and final global/non-fast SHA: `9b83aa1382d6b41c55981f2475eb0e236248affc5b5004a151a4b01651fa646e`
- C09 loaded: NO; C09 parameter/file identities were rejected as A2 initialisation.
- Approved config differences: four; unapproved differences: none.

## O08 online adaptation

O08 remained unchanged: LR 1e-3, 2 AdamW epochs, weight decay 1e-4, gradient clip 0.5, seed 20260816, exactly 165 fast values. Only the six authorised fast tensors were persisted in the online states.

| Symbol | Issued | Credits | Applied | Archived | Pending | Initial fast SHA | Final fast SHA | Final optimiser SHA |
|---|---:|---:|---:|---:|---:|---|---|---|
| AAPL | 26 | 26 | 23 | 2 | 1 | 49380bb69ea6fb7682fe97a3ef5e1ccf2b2429b749d6f9f9971e40725271fcf9 | bf1fd7555093781b94053883c47a8a1104361085cf85e174e86728546fa9d4af | 7577bca35d1d0a991ef27fea9fb85c93dde342355ce4e97ba3bbe1ab5e96edb4 |
| AMZN | 26 | 26 | 23 | 2 | 1 | 49380bb69ea6fb7682fe97a3ef5e1ccf2b2429b749d6f9f9971e40725271fcf9 | 3ee6338239854c27d236915440d4602955a7ecfcaf29bc22e0ae1e6fb94438e8 | 065284c80ed1b877974f8dc670532559b78031b549c687f178ba91a2296af3fa |
| JPM | 26 | 26 | 23 | 2 | 1 | 49380bb69ea6fb7682fe97a3ef5e1ccf2b2429b749d6f9f9971e40725271fcf9 | 0fc22f9c4d112c932524b74e328c2e3efbad1f690ac3691fb7a307bceca23135 | 5c46b84a03d7e31e34c3b7810975f74a393483438950d45125d42c7d1d3ece9f |

Global/non-fast mutations: 0. Unauthorised parameter mutations: 0. Cross-symbol mutations: 0. Duplicate updates: 0. Each applied update has one application ID, one event ID, and a pre/post fast identity.

## Delayed-credit chronology

Each symbol has 26 issued actions and credits: 23 APPLIED, 2 ARCHIVED, and 1 PENDING. The terminal 2024-06-28 credit remains PENDING because its fifth subsequent XNYS session is after the frozen 2024-07-05 horizon. Same-close chronology, no early maturity, exactly-once application, and symbol isolation all pass.

## Same-lineage recovery

Five EC2 auto-stop interruptions were safely resumed in the same lineage. Committed prefixes were 13, 28, 40, 55, and 70; final completion was the sixth run. Clean-unstarted boundaries were preserved; no torn rollback was needed. Committed cases regenerated: 0. Committed cases replaced: 0. Competing trajectories: 0. Four launch handoff retries created no run and made no paid call.

## Metrics

| Scope | Cumulative return | Excess vs B&H | Sharpe | Maximum drawdown | Calmar |
|---|---:|---:|---:|---:|---:|
| AAPL | 0.0000000 | -0.24445791 | null | 0.0000000 | null |
| AMZN | 0.36159290 | 0.0000000 | 2.6664860 | 0.081354164 | 10.724545 |
| JPM | 0.0000000 | -0.20266860 | null | 0.0000000 | null |
| equal_weight_aggregate | 0.12053097 | -0.14904217 | 2.5717451 | 0.031854296 | 8.1686770 |

The aggregate excess value is versus the equal-weight mean of the three stock buy-and-hold returns. Full secondary metrics are preserved in the official bundle.

## Usage and resources

DeepSeek V4 Flash usage across the complete same-lineage record: 2298 request records, 24501677 input tokens, 3053112 output tokens, 27554789 total tokens, CNY 22.87189076. Of these, 234 were live requests and 2064 were cache-origin replay records. No failed/partial usage record was produced; no unquantified request is estimated.

AWS accounting uses six successful starts, zero capacity failures, five preserved 90-minute auto-stop windows, and the final explicit window: 30724 running seconds (8.53444444 GPU-hours), estimated USD 10.89848556 at USD 1.277/hour. The canonical instance is stopped with zero running or pending AlphaMAS g5.xlarge instances.

## Archive and secret scan

- Archive: `experiments/A2/formal/official_bundle/A2_no_global_pretraining_2024H1`
- S3 bundle: `s3://alphamas-m2-eu-west-2-c9f1eaf2-671/a2/formal/20260818T204749061036Z_ae0f36b1/a2_formal_bundle.tar.gz`
- Remote/local bundle SHA: `6ee493f233b3635f682b0a08a697986a6169717330a0d5a1577c95f46f6ed149`
- Inventory: `experiments/A2/formal/A2_SHA256SUMS`
- Inventory SHA: `0106e17ddba6bde6687ee0ea5cd5f3ac06210f466c028b40033bac78615adcc3` (7631 entries)
- SHA verification: 7,631/7,631 OK; hash mismatch 0
- Missing 0; duplicate cases 0; invalid JSON 0; source/config identity mismatch 0
- DeepSeek credential archived: NO
- AWS credential archived: NO
- `.env` included: NO
- Private-key pattern matches: 0

No ARMA or COMPARE-01 work was started.
