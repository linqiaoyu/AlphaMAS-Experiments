# M2 Final Post-run Audit

Generated at `2026-08-17T12:07:04Z` from the remotely verified archive commit
`63b2ed2d98d954b4eaa7815c08f1e9fdef8aa4e0` and the frozen AlphaMAS source
`6306ea4ea20cda501c6238db80c34d27bbc16bea`.

## Verdict

The official `M2_agentic_rl_2024H1` result passes the final read-only audit. The
official run is `20260817T101217082243Z_6306ea4e` with AAPL 26, AMZN 26, and JPM
26 decisions (78 total), zero decision failures, and a passed Formal validation
report.

## Correctness and integrity

- The 26 weekly XNYS close decisions per symbol, next-valid-session open
  executions, Good Friday handling, and final `2024-07-05` valuation are valid.
- Source-audit records contain no future-visible event, same-bar execution,
  FINAL_HOLDOUT leakage, live-data substitution, or raw FinMultiTime regeneration.
- The portfolio contract remains $100,000 initial cash per symbol, fractional
  long-only shares, no shorting or leverage, BUY=100%, SELL=0%, HOLD=preserve,
  5 bps commission, 5 bps slippage, daily marking, and no terminal liquidation.
- The archive has exactly 78 unique DecisionCache cases. Prompt Trader, frozen
  M2 Actor, Risk Debate, Portfolio Manager, final execution mapping, usage,
  Memory, orders, fills, equity, metrics, and validation provenance is complete.
- All 12,058 SHA-256 inventory entries match. All 4,364 JSON documents parse.
  There are no missing, duplicate, unexpected, or unlisted Formal case files.
- The exact known DeepSeek credential value and generic AWS, private-key, and
  provider-token patterns have zero matches in current tracked artifacts. The
  known value also has zero Git-history matches in both repositories.

## Delayed-credit chronology

Each symbol has 26 issued actions and credits: 23 exactly-once `APPLIED`, two
`ARCHIVED`, and one `PENDING`. Every applied credit has exactly one matching
update record; there are no duplicate, orphan, or cross-symbol applications.
The AAPL, AMZN, and JPM `2024-06-28` credits each mature on `2024-07-08`, beyond
the frozen `2024-07-05` market horizon, and remain correctly `PENDING`.

## Same-lineage recovery

The archive preserves 11 operational attempts: one initial attempt and ten safe
resumes after ten interruptions. Every manifest is bound to the same experiment,
source SHA, and Memory lineage `20260816T150158003630Z_6306ea4e`; the resume chain
terminates at the official run. No competing top-level official trajectory exists.
Torn runtime states were restored only after exact pre-case proofs. Completed
cases regenerated: 0. Completed cases replaced: 0. Historical failure evidence
remains preserved.

## Resource accounting

Complete recoverable same-lineage DeepSeek usage is 2,345 requests, 24,961,617
input tokens, 3,127,030 output tokens, and CNY 24.08240596. This includes 2,308
requests attached to the 78 committed cases and 37 recorded requests from two
partial failed attempts. The final 76-to-78 resume remains separately identified
as 58 requests and CNY 0.53880224. Requests interrupted before a usage record
could be flushed cannot be proven absent and are explicitly not estimated.

CloudTrail records ten successful starts and 27 capacity-failure API events,
representing nine logical failed start commands after AWS CLI retries. Preserved
start/stop and 90-minute auto-stop evidence gives an estimated 38,319 running
seconds (10.64416667 GPU-hours), or USD 13.59260083 at the AWS Price List on-demand
rate of USD 1.277/hour. The final 76-to-78 resume is separately 3,266 seconds,
0.90722222 GPU-hours, and USD 1.15851806. The canonical instance is stopped and
there are zero running or pending AlphaMAS `g5.xlarge` instances.

## Frozen identities and branches

C09, O08, the M1 bundle, semantic representation, R3 reward, method, and TRAIN
counterfactual-tree identities all match their frozen records. The authoritative
A1/A2 preregistration identity remains
`e7e2cc8520f9033e57c442b04c882baffd7c51b497bbc9495b71098f64a83b0e`.

The remote refs `baseline-m2`, `ablation/a1-no-online-adaptation`, and
`ablation/a2-no-global-pretraining` all point exactly to
`6306ea4ea20cda501c6238db80c34d27bbc16bea`. A1 and A2 therefore have zero
implementation delta in M2-16. The legacy ablation branches were not changed.

The regression suite passed 542 relevant checks; one legacy pilot-only fixture
was unavailable, while the frozen Formal M1 inputs and all selected M1, PIT,
backtesting, M2, semantic-state, delayed-credit, safe-resume, and A1/A2 contract
checks ran successfully. The repository's read-only Formal artifact validator
also passed without any reported error.
